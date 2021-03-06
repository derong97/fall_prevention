
#Remove previous values
rm(list=ls())

#Import the excel file
data <- read.csv("C:\\Users\\Gan Yu\\Documents\\SUTD ESD Term 8 Learning Materials\\Capstone 2\\data_r_codes_4.csv")

#Create new columns
data$sit_total <- rep(0,nrow(data))
data$bend_total <- rep(0,nrow(data))
data$stand_total <- rep(0,nrow(data))
data$tampered_total <- rep(0,nrow(data))
data$inaction_total <- rep(0,nrow(data))
data$predicted_label <- rep(0,nrow(data))

#Set threshold values
i <- 1
thermal_weight <- 0.68
weight_weight <- 1-thermal_weight
w_f_decrease_inaction <- -201.4796499
w_f_increase_bend_stand <- 149.2184482
w_b_decrease_bend_stand <- -77.02051206
w_f_decrease_sit <- -149.2184482
w_b_increase_sit <- 77.02051206

while (data$expt_no[i] < 30)
{
  if (data$sit_probability[i] > max(data$bend_probability[i], data$stand_probability[i], data$tampered_probability[i], data$inaction_probability[i]))
  {
    if (data$w_b_change[i] < w_b_decrease_bend_stand | data$w_f_change[i] > w_f_increase_bend_stand)
    {
      data$sit_total[i] <- data$sit_probability[i]*thermal_weight
      data$bend_total[i] <- data$bend_probability[i]*thermal_weight + weight_weight
      data$stand_total[i] <- data$stand_probability[i]*thermal_weight + weight_weight
      data$tampered_total[i] <- data$tampered_probability[i]*thermal_weight + weight_weight
      data$inaction_total[i] <- data$inaction_probability[i]*thermal_weight
      if (data$sit_total[i] > max(data$bend_total[i], data$stand_total[i], data$tampered_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 0
      }
      else if (data$bend_total[i] > max(data$sit_total[i], data$stand_total[i], data$tampered_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 1
      }
      else if (data$stand_total[i] > max(data$sit_total[i], data$bend_total[i], data$tampered_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 1
      }
      else if (data$tampered_total[i] > max(data$sit_total[i], data$bend_total[i], data$stand_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 1
      }
    }
    else
    {
      data$sit_total[i] <- data$sit_probability[i]*thermal_weight + weight_weight
      data$bend_total[i] <- data$bend_probability[i]*thermal_weight
      data$stand_total[i] <- data$stand_probability[i]*thermal_weight 
      data$tampered_total[i] <- data$tampered_probability[i]*thermal_weight
      data$inaction_total[i] <- data$inaction_probability[i]*thermal_weight
    }
  }
  else if (data$bend_probability[i] > max(data$stand_probability[i], data$tampered_probability[i], data$inaction_probability[i]))
  {
    if (data$w_f_change[i] < w_f_decrease_inaction)
    {  
      data$sit_total[i] <- data$sit_probability[i]*thermal_weight
      data$bend_total[i] <- data$bend_probability[i]*thermal_weight
      data$stand_total[i] <- data$stand_probability[i]*thermal_weight 
      data$tampered_total[i] <- data$tampered_probability[i]*thermal_weight
      data$inaction_total[i] <- data$inaction_probability[i]*thermal_weight + weight_weight
      if (data$bend_total[i] > max(data$sit_total[i], data$stand_total[i], data$tampered_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 1
      }
      else if (data$inaction_total[i] > max(data$sit_total[i], data$bend_total[i], data$stand_total[i], data$tampered_total[i]))
      {
        data$predicted_label[i] <- 3
      }
    }
    else if (data$w_b_change[i] > w_b_increase_sit | data$w_f_change[i] < w_f_decrease_sit)
    {
      data$sit_total[i] <- data$sit_probability[i]*thermal_weight + weight_weight
      data$bend_total[i] <- data$bend_probability[i]*thermal_weight
      data$stand_total[i] <- data$stand_probability[i]*thermal_weight 
      data$tampered_total[i] <- data$tampered_probability[i]*thermal_weight
      data$inaction_total[i] <- data$inaction_probability[i]*thermal_weight
      if (data$sit_total[i] > max(data$bend_total[i], data$stand_total[i], data$tampered_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 0
      }
      else if (data$bend_total[i] > max(data$sit_total[i], data$stand_total[i], data$tampered_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 1
      }
    }
    else
    {
      data$sit_total[i] <- data$sit_probability[i]*thermal_weight
      data$bend_total[i] <- data$bend_probability[i]*thermal_weight
      data$stand_total[i] <- data$stand_probability[i]*thermal_weight 
      data$tampered_total[i] <- data$tampered_probability[i]*thermal_weight
      data$inaction_total[i] <- data$inaction_probability[i]*thermal_weight
      data$predicted_label[i] <- 1
    }
  }
  else if (data$stand_probability[i] > max(data$tampered_probability[i], data$inaction_probability[i]))
  {
    if (data$w_f_change[i] < w_f_decrease_inaction)
    {
      data$sit_total[i] <- data$sit_probability[i]*thermal_weight
      data$bend_total[i] <- data$bend_probability[i]*thermal_weight
      data$stand_total[i] <- data$stand_probability[i]*thermal_weight 
      data$tampered_total[i] <- data$tampered_probability[i]*thermal_weight
      data$inaction_total[i] <- data$inaction_probability[i]*thermal_weight + weight_weight
      if (data$stand_total[i] > max(data$sit_total[i], data$bend_total[i], data$tampered_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 1
      }
      else if (data$inaction_total[i] > max(data$sit_total[i], data$bend_total[i], data$stand_total[i], data$tampered_total[i]))
      {
        data$predicted_label[i] <- 3
      }
    }
    else if (data$w_b_change[i] > w_b_increase_sit | data$w_f_change[i] < w_f_decrease_sit)
    {
      data$sit_total[i] <- data$sit_probability[i]*thermal_weight + weight_weight
      data$bend_total[i] <- data$bend_probability[i]*thermal_weight
      data$stand_total[i] <- data$stand_probability[i]*thermal_weight 
      data$tampered_total[i] <- data$tampered_probability[i]*thermal_weight
      data$inaction_total[i] <- data$inaction_probability[i]*thermal_weight
      if (data$sit_total[i] > max(data$bend_total[i], data$stand_total[i], data$tampered_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 0
      }
      else if (data$stand_total[i] > max(data$sit_total[i], data$bend_total[i], data$tampered_total[i], data$inaction_total[i]))
      {
        data$predicted_label[i] <- 1
      }
    }
    else
    {
      data$sit_total[i] <- data$sit_probability[i]*thermal_weight
      data$bend_total[i] <- data$bend_probability[i]*thermal_weight
      data$stand_total[i] <- data$stand_probability[i]*thermal_weight + weight_weight
      data$tampered_total[i] <- data$tampered_probability[i]*thermal_weight
      data$inaction_total[i] <- data$inaction_probability[i]*thermal_weight
      data$predicted_label[i] <- 1
    }
  }
  else if (data$inaction_probability[i] > data$tampered_probability[i])
  {
    data$predicted_label[i] <- 3
  }
  else
  {
    data$predicted_label[i] <- 1
  }
  i <- i + 1
}

#Check confusion matrix
table <- table(data$label, data$predicted_label)
table

#Determine accuracy
Accuracy <- sum(diag(table))/nrow(data)
Accuracy

#Export to Excel file
write.table(data,file="Predict_Label.csv",sep=",")
