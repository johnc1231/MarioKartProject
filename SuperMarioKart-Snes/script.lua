function reward() 
    lap = data.Lap - 127
    weighted_lap = lap * 1000
    pos = data.POS --This varies between 0 and 40 or so, depending on track. 
    weighted_pos = pos * 10
    speed = data.OverallSpeed -- this varies between 0 and 1000
    weighted_speed = (speed / 100) 


    return weighted_lap + weighted_pos + weighted_speed
end