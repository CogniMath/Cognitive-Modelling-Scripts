actr.a = 1.1
actr.b = 0.015
actr.t0 = 11

num.subjects = 5
num.sessions = 3
num.trials = 500
num.values = 11

printf <- function(...) print(sprintf(...))

create.dm <- function(chunks,encounters)
{
  if (chunks > 52)
  {
    stop("Only up to 52 chunks allowed.")
  }
  DM <- array(NA,c(chunks,encounters))
  row.names(DM) <- c(letters,LETTERS)[1:chunks]
  
  return (DM)
}

add.encounter <- function(DM,chunk,time)
{
  tmp <- DM[chunk,]
  DM[chunk,sum(!is.na(tmp))+1] <- time
  
  return (DM)
}

get.encounters <- function(DM,chunk)
{
  tmp <- DM[chunk,]
  tmp[!is.na(tmp)]
}

actr.B <- function(encounters,curtime)
{
  if (curtime < min(encounters))
  {
    return(NA)
  }
  else
  {
    log(sum((curtime - encounters[encounters<curtime])^-params$d))
  }
}


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

run.trials <- function(int1, int2,DM)
{
  interval.vector <- seq(int1, int2, length.out=num.values)
  time.vector <- sample(interval.vector, num.trials, replace=T)  # create and store the randomly generated intervals
  
  chunk.names <- c(letters,LETTERS)[1:25]
  
  get.activation <- function(cl)
  {
    num.encounters <- get.encounters(dm, cl)
    activation <- actr.B(num.encounters, clock.time)
    
    return (activation)
  }
  
  for (sample.interval in time.vector)
  {
    # print(sample.interval)
    # print(time.vector)
    clock.time <- clock.time + 1000 + runif(1, 250, 850) + sample.interval # update of the "clock" according to the experience of the participants in the paper
    pulse <- time_into_pulse(sample.interval) # classic pulse into time function
    chunk.letter <- c(letters,LETTERS)[pulse] # save the results in a vector of letters for the DM
    
    # print(pulse)
    # print(chunk.letter)
    
    DM <- add.encounter(DM, chunk.letter, clock.time) # add the results to the DM
    
    # print(DM)
    
    all.activations <- sapply(1:chunk.names, get.activation)
    max.activation <- max(all.activations[!is.na(all.activations)])  # get the highest activation
    index <- match(max.activation,all.activations)
    
    print(index)
  }
}

experiment <- function(sub, trials)
{
  for (i in 1:num.subjects)
  {
    clock.time <- 0  # initialize clock to 0
    DM <- create.dm(25,num.trials*num.sessions*3) # size of the DM
    condition.type <- floor(runif(1,1,3))
    print(condition.type)
    
    for (cond in condition.type) {
      if (condition.type == 1)  #short experimental condition
      {
        run.trials(494, 847,DM)
      }
      
      else if (condition.type == 2) #intermidiate experimental condition
      {
        run.trials(671, 1023,DM)
      }
      
      else if(condition.type == 3)
      {
        run.trials(847, 1200,DM)  #long experimental condition
      }
    }
  }
}

my_main <- function()
{
  
  experiment(num.subjects, num.trials)
  run.trials(num.subjects, num.trials)
  
}

my_main()