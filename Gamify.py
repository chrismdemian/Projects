def initialize():
    global cur_hedons, cur_health
    global cur_time, last_activity, last_activity_end_time
    global stars_offered, last_star_time, bored_with_stars
    global star_activity, star_duration
    
    cur_hedons = 0
    cur_health = 0
    cur_time = 0
    last_activity = None
    last_activity_end_time = -float('inf')
    stars_offered = 0
    last_star_time = -float('inf')
    bored_with_stars = False
    star_activity = None
    star_duration = 0

def perform_activity(activity, duration):
    global cur_hedons, cur_health
    global cur_time, last_activity, last_activity_end_time
    global star_activity, star_duration, bored_with_stars
    
    if activity not in ['running', 'textbooks', 'resting']:
        return
    
    end_time = cur_time + duration
    
    if activity == 'running' or activity == 'textbooks':
        if last_activity_end_time + 120 > cur_time:
            tired = True
        else:
            tired = False
    
        health_increment = 0
        hedons_increment = 0
        
        if activity == 'running':
            health_increment = 3 * min(180, duration) + max(0, duration - 180)
            if tired:
                hedons_increment = -2 * duration
            else:
                hedons_increment = 2 * min(10, duration) + -2 * max(0, duration - 10)
                
        elif activity == 'textbooks':
            health_increment = 2 * duration
            if tired:
                hedons_increment = -2 * duration
            else:
                hedons_increment = 1 * min(20, duration) + -1 * max(0, duration - 20)
        
        if star_activity == activity and cur_time == last_star_time:
            hedons_increment += 3 * min(10, duration)
            star_duration = max(0, star_duration - duration)
            if star_duration <= 0:
                star_activity = None
        
    elif activity == 'resting':
        hedons_increment = 0
        health_increment = 0
    
    cur_hedons += hedons_increment
    cur_health += health_increment
    cur_time += duration
    last_activity = activity
    last_activity_end_time = end_time

def offer_star(activity):
    global cur_time, last_star_time, stars_offered, star_activity, star_duration, bored_with_stars
    
    if activity not in ['running', 'textbooks']:
        return
    
    if bored_with_stars:
        return
    
    stars_offered += 1
    last_star_time = cur_time
    star_activity = activity
    star_duration = 10
    
    if stars_offered == 3:
        if cur_time - last_star_time <= 7200:
            bored_with_stars = True

def get_cur_hedons():
    global cur_hedons
    return cur_hedons

def get_cur_health():
    global cur_health
    return cur_health

def star_can_be_taken(activity):
    global star_activity, cur_time, last_star_time
    return star_activity == activity and cur_time == last_star_time and not bored_with_stars

def most_fun_activity_minute():
    global last_activity_end_time, cur_time, bored_with_stars

    time_since_last_activity = cur_time - last_activity_end_time

    running_hedons = 2 if time_since_last_activity > 120 else -2
    textbooks_hedons = 1 if time_since_last_activity > 120 else -2
    resting_hedons = 0

    if star_activity and not bored_with_stars:
        if star_activity == 'running' and star_duration > 0:
            running_hedons += 3
        elif star_activity == 'textbooks' and star_duration > 0:
            textbooks_hedons += 3

    if running_hedons > textbooks_hedons and running_hedons > resting_hedons:
        return 'running'
    elif textbooks_hedons > running_hedons and textbooks_hedons > resting_hedons:
        return 'textbooks'
    else:
        return 'resting'