actr.a = 1.1
actr.b = 0.015
actr.t0 = 11
experiment.short_interval = 3
experiment.long_interval = 6

printf <- function(...) print(sprintf(...)) #My own printf function in order to debug

actr.noise <- function(s,n=1)
{
  rand <- runif(n,min=0.0001,max=0.9999)
  s * log((1 - rand ) / rand)
}

time_into_pulse <- function(time)
{
  interval_estimation <- actr.t0
  num_pulses <- 0
  time_tracker <- actr.t0
  
  while(time_tracker < time)
  {
    interval_estimation <- interval_estimation * actr.a + actr.noise(actr.a * actr.b* interval_estimation)
    time_tracker <-  time_tracker + interval_estimation
    num_pulses <- num_pulses +1
  }
  
  return (num_pulses)
  
}

existing_data <- function()
{
  
  time = c(3, 3.37, 3.78, 4.24, 4.76, 5.34, 6)
  proportion_long = c(0.08, 0.1, 0.2, 0.45, 0.74, 0.86, 0.95)
  existing_data <- data.frame(time, proportion_long)
  
  return(existing_data)
  
}

drawPlot <- function(short_interval, long_interval, real_data, subjectResults) {
  # Returns a function which rounds to the nearest given multiple.
  roundingGenerator <- function(nearest) {
    function(v) {
      f = 1 / nearest
      round(v * f) / f
    }
  }
  
  numDataPoints = 7  # how many bins to group data into
  roundingValue = (long_interval - short_interval) / (numDataPoints - 1) * 1000
  rounder = roundingGenerator(roundingValue)
  
  # loop over participants and store ratios between short/long frequencies per bin
  binnedResults = c()
  for(pIndex in 1:dim(subjectResults)[3]) {
    testDurations = subjectResults[,1,pIndex]
    testClassifications = subjectResults[,2,pIndex]
    
    # Round the original test durations to the nearest 1/2 second so we can bin them.
    testDurations = rounder(testDurations)
    
    # Create an object with both the durations and how they were classified.
    durationsWithClass = cbind(testDurations, testClassifications)
    
    # Create a sorted list of unique durations. The for each binned duration, calculate the ratio between trials judged as short and long.
    durations = sort(unique(testDurations))
    ratios = sapply(durations, function (v) {
      shortCount = length(subset(durationsWithClass, durationsWithClass[,1] == v & durationsWithClass[,2] == 0))
      longCount = length(subset(durationsWithClass, durationsWithClass[,1] == v & durationsWithClass[,2] == 1))
      ratio = longCount / (shortCount + longCount)
      
      # printf("short/long counts for %i: %i/%i (%.2f)", v, shortCount, longCount, ratio)
      return(ratio)
    })
    
    binnedResults = cbind(binnedResults, ratios)
  }
  
  meanRatios = rowMeans(binnedResults)
  times = seq(short_interval, long_interval, length.out=numDataPoints)
  plotData = cbind(times, meanRatios)
  
  # And finally plot it.
  title = sprintf("%g to %s sec discrimination", short_interval, long_interval)
  par(pch=6, lty=2)
  plot(plotData, type="b", main=title, xlab="Time (s)", ylab="Proportion long", ylim=c(0.0, 1.0))
  lines(real_data, type="b", pch=5, lty=1)
  legend('bottomright', c("simulation", "real"), lty=c(2,1), pch=c(6,5))
}

training_phase <- function(short_interval, long_interval)
{
  short_time <- c()
  long_time <- c()
  
  for (i in 1:(10/2))
  {
    short_time <- c(short_time, time_into_pulse(short_interval*1000))
    long_time <- c(long_time,time_into_pulse(long_interval*1000))
  }
  
  mean_short_time <- mean(short_time)
  mean_long_time <- mean(long_time)
  means <- c(mean_short_time, mean_long_time)
  
  return(means)
  
}

checking_method <- function(pulse_count, mean_short_time, mean_long_time)
{
  
  if (abs(mean_short_time - pulse_count) < abs(mean_long_time - pulse_count))
  {
    return (0) #0 means it has been classified as short
  }
  else
  {
    return (1) #1 means it has been classified as long
  }
}

testing_phase <- function(short_interval, long_interval, mean_short_time, mean_long_time)
{
  num_participants <- 50
  num_test_trials <- 100
  
  participant_data <- c()
  total_time_phases <- c()
  total_time_estimations <- c()
  
  for (i in 1:num_participants)
  {
    time_phases <- c()
    time_estimations <- c()
    
    for (j in 1:num_test_trials)
    {
      value <- runif(1, 0, 99)
      
      if(value < 15)
      {
        interval <- short_interval*1000;
      }
      
      else if(value < 30)
      {
        interval <- long_interval*1000;
      }
      
      else
      {
        interval <- runif(1, 3, 6)*1000
      }
      
      time_phases <- c(time_phases, interval)
      pulse_count <- time_into_pulse(interval)
      time_estimations <- c(time_estimations, checking_method(pulse_count, mean_short_time, mean_long_time))
    }
    
    participant_data <- c(participant_data, cbind(time_phases, time_estimations))
    total_time_phases <- c(total_time_phases, time_phases)
    total_time_estimations <- c(total_time_estimations, time_estimations)
    
  }
  
  plot_array <- array(participant_data, dim=c(num_test_trials, 2, num_participants))
  real_data <- data.frame(c(3, 3.37, 3.78, 4.24, 4.76, 5.34, 6), c(0.08, 0.1, 0.2, 0.45, 0.74, 0.86, 0.95))
  drawPlot(3, 6, real_data, plot_array)
}

my_main <- function()
{
  
  existing_data <- existing_data()
  plot(existing_data)
  means <- training_phase(experiment.short_interval, experiment.long_interval)
  testing_phase(experiment.short_interval, experiment.long_interval, means[1], means[2])
  
}

my_main()