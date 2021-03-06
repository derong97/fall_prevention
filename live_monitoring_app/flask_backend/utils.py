import numpy as np

#Setting threshold values
thermal_weight = 0.68
weight_weight = 1 - thermal_weight
w_f_decrease_inaction = -201.4796499
w_f_increase_bend_stand = 149.2184482
w_b_decrease_bend_stand = -77.02051206
w_f_decrease_sit = -149.2184482
w_b_increase_sit = 77.02051206


def get_alert(posture_label, preemptive_label):
    if posture_label == 0: # sit
        if preemptive_label == 1: # performed preemptive actions
            return "mod"
        return "low"
    elif posture_label == 1: # get up, stand
        return "high"
    elif posture_label == 3: # fall
        return "fall"

def get_preemptive_label(v_b, v_t):
    if v_b + v_t >= 3:
        return 1    
    return 0    
    
def get_posture_label(sit_score, bend_score, stand_score, tampered_score, inaction_score,
                        w_bl, w_br, w_fl, w_fr, previous_state_w_b=0, previous_state_w_f=0):
    w_b_sum = w_bl + w_br
    w_f_sum = w_fl + w_fr
    
    w_b_change = w_b_sum - previous_state_w_b
    w_f_change = w_f_sum - previous_state_w_f
    sit_probability = np.exp(sit_score)
    bend_probability = np.exp(bend_score)
    stand_probability = np.exp(stand_score)
    tampered_probability = np.exp(tampered_score)
    inaction_probability = np.exp(inaction_score)
    sit_total = 0
    bend_total = 0 
    stand_total = 0 
    tampered_total = 0
    inaction_total = 0 
    predicted_label = 0
    if sit_probability > max(bend_probability, stand_probability, tampered_probability, inaction_probability):
        if (w_b_change < w_b_decrease_bend_stand or w_f_change > w_f_increase_bend_stand):
            sit_total = sit_probability*thermal_weight
            bend_total = bend_probability*thermal_weight + weight_weight
            stand_total = stand_probability*thermal_weight + weight_weight
            tampered_total = tampered_probability*thermal_weight + weight_weight
            inaction_total = inaction_probability*thermal_weight
            if sit_total > max(bend_total, stand_total, tampered_total, inaction_total):
                predicted_label = 0
            elif bend_total > max(sit_total, stand_total, tampered_total, inaction_total):
                predicted_label = 1
            elif stand_total > max(sit_total, bend_total, tampered_total, inaction_total):
                predicted_label = 1
            elif tampered_total > max(sit_total, bend_total, stand_total, inaction_total):
                predicted_label = 1
        else:
            sit_total = sit_probability*thermal_weight + weight_weight
            bend_total = bend_probability*thermal_weight
            stand_total = stand_probability*thermal_weight 
            tampered_total = tampered_probability*thermal_weight
            inaction_total = inaction_probability*thermal_weight
            predicted_label = 0
    elif bend_probability > max(stand_probability, tampered_probability, inaction_probability):
        if w_f_change < w_f_decrease_inaction:
            sit_total = sit_probability*thermal_weight
            bend_total = bend_probability*thermal_weight
            stand_total = stand_probability*thermal_weight 
            tampered_total = tampered_probability*thermal_weight
            inaction_total = inaction_probability*thermal_weight + weight_weight
            if bend_total > max(sit_total, stand_total, tampered_total, inaction_total):
                predicted_label = 1
            elif inaction_total > max(sit_total, bend_total, stand_total, tampered_total):
                predicted_label = 3
        elif w_b_change > w_b_increase_sit or w_f_change < w_f_decrease_sit:
            sit_total = sit_probability*thermal_weight + weight_weight
            bend_total = bend_probability*thermal_weight
            stand_total = stand_probability*thermal_weight 
            tampered_total = tampered_probability*thermal_weight
            inaction_total = inaction_probability*thermal_weight
            if sit_total > max(bend_total, stand_total, tampered_total, inaction_total):
                predicted_label = 0
            elif bend_total > max(sit_total, stand_total, tampered_total, inaction_total):
                predicted_label = 1
        else:
            sit_total = sit_probability*thermal_weight
            bend_total = bend_probability*thermal_weight
            stand_total = stand_probability*thermal_weight 
            tampered_total = tampered_probability*thermal_weight
            inaction_total = inaction_probability*thermal_weight
            predicted_label = 1
    elif stand_probability > max(tampered_probability, inaction_probability):
        if w_f_change < w_f_decrease_inaction:
            sit_total = sit_probability*thermal_weight
            bend_total = bend_probability*thermal_weight
            stand_total = stand_probability*thermal_weight 
            tampered_total = tampered_probability*thermal_weight
            inaction_total = inaction_probability*thermal_weight + weight_weight
            if stand_total > max(sit_total, bend_total, tampered_total, inaction_total):
                predicted_label = 1
            elif inaction_total > max(sit_total, bend_total, stand_total, tampered_total):
                predicted_label = 3
        elif w_b_change > w_b_increase_sit or w_f_change < w_f_decrease_sit:
            sit_total = sit_probability*thermal_weight + weight_weight
            bend_total = bend_probability*thermal_weight
            stand_total = stand_probability*thermal_weight 
            tampered_total = tampered_probability*thermal_weight
            inaction_total = inaction_probability*thermal_weight
            if sit_total > max(bend_total, stand_total, tampered_total, inaction_total):
                predicted_label = 0
            elif stand_total > max(sit_total, bend_total, tampered_total, inaction_total):
                predicted_label = 1
        else:
            sit_total = sit_probability*thermal_weight
            bend_total = bend_probability*thermal_weight
            stand_total = stand_probability*thermal_weight + weight_weight
            tampered_total = tampered_probability*thermal_weight
            inaction_total = inaction_probability*thermal_weight
            predicted_label = 1
    elif inaction_probability > tampered_probability:
        predicted_label = 3
    else:
      predicted_label = 1
    
    previous_state_w_b = w_b_sum
    previous_state_w_f = w_f_sum
    
    return predicted_label, previous_state_w_b, previous_state_w_f