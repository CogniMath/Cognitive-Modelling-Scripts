actr.a = 1.1
actr.b = 0.0
actr.t0 = 11

printf <- function(...) print(sprintf(...))

actr.noise <- function(s,n=1)
{
  rand <- runif(n,min=0.0001,max=0.9999)
  s * log((1 - rand ) / rand)
}

pulse_into_time <- function(num_pulses)
{
  interval_estimation <- actr.t0
  global_time <- actr.t0
  
  for (i in 1:num_pulses)
  {
    interval_estimation <- interval_estimation * actr.a + actr.noise(actr.a * actr.b* interval_estimation)
    global_time <- global_time + interval_estimation
  }
  
  return (global_time)
  
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

my_main <- function()
{
  for (i in 1:10)
  {
    global_time <- pulse_into_time(i)
    num_pulses <- time_into_pulse(global_time)
    
    printf("Current_Pulse %g, Global_Time %g, Converted_Pulse %g", i, global_time, num_pulses)
    
  }

}

my_main()