# This is the Console version of the App
# is not the major version

from os import name
import pandas as pd

# file = input("Enter the csv file name:")
# df = pd.read_csv(f"{file}.csv")

# ---------------Technical_Block----------------------
# Load Users data
def load_data():
    global df_users, df_activities, df_rewards, df_achievements
    df_users = pd.read_csv('users.csv')
    df_activities = pd.read_csv('activities.csv')
    df_rewards = pd.read_csv('rewards.csv')
    df_achievements = pd.read_csv('achievements.csv')

    return 'Data loaded successfully!'

# Sorting function in ascending order by points/prices
def quick_sort_by_points(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2][1]
    left = [x for x in arr if x[1] < pivot]
    middle = [x for x in arr if x[1] == pivot]
    right = [x for x in arr if x[1] > pivot]

    return quick_sort_by_points(left) + middle + quick_sort_by_points(right)
# -------------------------------------

# At the moment of initilizing user should provide its own lists
class Activity:
    def __init__(self, activity_names=None, activity_points=None, daily_task=None):
        #  If the user doesn't provide a list, that list is used by default
        if activity_names is None:
            activity_names = df_activities.loc[:, 'activity_name'].tolist()
        #  If the user does provide a list, that list is used instead of default one
        self.activity_names = activity_names
        # Same here:
        if activity_points is None:
            activity_points = df_activities.loc[:, 'activity_points'].tolist()
        self.activity_points = activity_points
        if daily_task is None:
            daily_task = df_activities.loc[:, 'daily_task'].tolist()
        self.daily_task = daily_task
        
        
        
    def show_activities(self):
        print('Available Activities:\n')
        
        daily_arr = []
        misc_arr = []

        # Collect tasks into arrays
        for name, points, is_daily in zip(self.activity_names, self.activity_points, self.daily_task):
            if is_daily:
                daily_arr.append((name, points))
            else:
                misc_arr.append((name, points))
        
        # Sort both arrays by points (ascending)
        daily_arr = quick_sort_by_points(daily_arr)
        misc_arr = quick_sort_by_points(misc_arr)
        
        # Display daily tasks
        print('Daily Tasks:')
        for i in range(len(daily_arr)):
            print(f'{i + 1}. {daily_arr[i][0]} ({daily_arr[i][1]} points)')

        # Display miscellaneous tasks
        print('\nMiscellaneous:')
        for i in range(len(misc_arr)):
            print(f'{i + 1}. {misc_arr[i][0]} ({misc_arr[i][1]} points)')


# Similar to Activity class in terms of initialization
class Reward:
    def __init__(self, reward_names=None, reward_prices=None, regular_reward=None):
        if reward_names is None:
            reward_names = df_rewards.loc[:, 'reward_name'].tolist()
        self.reward_names = reward_names
        if reward_prices is None:
            reward_prices = df_rewards.loc[:, 'reward_price'].tolist()
        self.reward_prices = reward_prices
        if regular_reward is None:
            regular_reward = df_rewards.loc[:, 'regular_reward'].tolist()
        self.regular_reward = regular_reward
        
        
    def show_rewards(self):
        
        print('Available Rewards:\n')
        reg_arr = []
        long_term_arr = []
        
        for name, price, is_regular in zip(self.reward_names, self.reward_prices, self.regular_reward):
            if is_regular:
                reg_arr.append((name, price))
            else:
                long_term_arr.append((name, price))
                
        # Sort both arrays by prices (ascending)
        reg_arr = quick_sort_by_points(reg_arr)
        long_term_arr = quick_sort_by_points(long_term_arr)
        
        # Display regular rewards
        print('Regular Rewards:')
        for i in range(len(reg_arr)):
            print(f'{i + 1}. {reg_arr[i][0]} ({reg_arr[i][1]} points)')
            
        # Display long-term rewards
        print('\nLong-term Rewards:')
        for i in range(len(long_term_arr)):
            print(f'{i + 1}. {long_term_arr[i][0]} ({long_term_arr[i][1]} points)')
        
class Achievement:
    def __init__(self, achievement_names=None, points_required=None, tasks_required=None):
        if achievement_names is None:
            achievement_names = df_achievements.loc[:, 'achievement_name'].tolist()
        self.achievement_names = achievement_names
        if points_required is None:
            points_required = df_achievements.loc[:, 'points_required'].tolist()
        self.points_required = points_required
        if tasks_required is None:
            tasks_required = df_achievements.loc[:, 'tasks_required'].tolist()
        self.tasks_required = tasks_required
            
    def show_achievements(self):
        print('Available Achivements: ')
        i = 0
        for achivement, points, tasks in zip(self.achievement_names, self.points_required, self.tasks_required):
            i += 1
            print(f'{i}. {achivement} ({points} points OR {tasks} completed tasks)')
    
class User:
    def __init__(self, name, total_points=0, activities_completed=0, alltime_points=0):
        self.name = name
        self.total_points = total_points
        self.activities_completed = activities_completed
        self.alltime_points = alltime_points
    
    #------------CSV_File_Managment---------------
    def add_user(self):
        new_user = pd.DataFrame([[self.name, self.total_points, self.activities_completed, self.alltime_points]], columns=['name', 'total_points', 'activities_completed', 'alltime_points'])
        df_users.to_csv('users.csv', index=False, mode='a', header=False)

        return f'{self.name} added successfully!'

    def update_user(self):
        df_users.loc[df_users['name'] == self.name, 'total_points'] = self.total_points
        df_users.loc[df_users['name'] == self.name, 'activities_completed'] = self.activities_completed
        df_users.loc[df_users['name'] == self.name, 'alltime_points'] = self.alltime_points
        df_users.to_csv('users.csv', index=False)

        return f'User \"{self.name}\" is updated successfully!'
    
    def delete_user(self):
        df_users.drop(index=[self.name], inplace=True)
        df_users.to_csv('users.csv', index=False)

        return f'{self.name} deleted successfully!'
    #----------------------------------------------
    
    def complete_activity(self, activity: Activity):
        act_num = int(input('Enter the activity number you have completed: '))
        if 0 < act_num < len(activity.activity_names)+1:
            self.total_points += activity.activity_points[act_num - 1]
            self.alltime_points += activity.activity_points[act_num - 1]
            self.activities_completed += 1
            print(f'Activity "{activity.activity_names[act_num - 1]}" completed! You earned {activity.activity_points[act_num - 1]} points.')
        else:
            print(f'{act_num} is invalid activity number!')
    
    def redeem_reward(self, reward: Reward):
        rwd_num = int(input('Enter the reward number you would like to redeem: '))
        if 0 < rwd_num < len(reward.reward_names)+1:
            if self.total_points < reward.reward_prices[rwd_num - 1]:
                print(f'You have not enough points to redeem the reward \"{reward.reward_names[rwd_num - 1]}\"!')
                return
            self.total_points -= reward.reward_prices[rwd_num - 1]
            print(f'Reward "{reward.reward_names[rwd_num - 1]}" successfully redeemed! You spent {reward.reward_prices[rwd_num - 1]} points.')
            print(f'You have {self.total_points} points left.')
        else:
            print(f'{rwd_num} is invalid reward number!')
    
    def define_rank(self, achievement: Achievement):
        # Determine rank based on points and activities completed
        for i in range(len(achievement.achievement_names)):
            if self.alltime_points < achievement.points_required[i] and self.activities_completed < achievement.tasks_required[i]:
                return achievement.achievement_names[i-1]
        # Return last rank if any threshold is met for the highest rank
        return achievement.achievement_names[-1]
            
    def show_status(self):
        print('----------------Status:-----------------------')
        print(f"Currently you have : {self.total_points} points.")
        print(f"Total Activities Completed : {self.activities_completed}")
        print(f"All-time Points Earned : {self.alltime_points}")
        print(f"You're current rank is: {self.define_rank(test_acv)}")
        print('----------------------------------------------')
    

class Manager:
    def __init__(self):
        pass
    
    def add_activity(self, activity_name, activity_points, daily_task):
        
        if daily_task.lower() in ['yes', 'y', 'true', '1']:
            daily_task = True
        elif daily_task.lower() in ['no', 'n', 'false', '0']:
            daily_task = False
        else:
            return f'Error: Invalid input for daily_task. Please enter "yes" or "no".'
        
        new_activity = pd.DataFrame([[activity_name, activity_points, daily_task]], columns = ['activity_name', 'activity_points', 'daily_task'])
        # Ensure the CSV file ends with a newline before appending to avoid concatenation with the last line
        try:
            with open('activities.csv', 'rb+') as f:
                f.seek(0, 2)
                if f.tell() > 0:
                    f.seek(-1, 2)
                    last = f.read(1)
                    if last != b'\n':
                        f.write(b'\n')
        except FileNotFoundError:
            # File doesn't exist yet, to_csv will create it
            pass

        new_activity.to_csv('activities.csv', index=False, mode='a', header=False)
        return f'Activity \"{activity_name}\" added successfully!'

    def add_reward(self, reward_name, reward_price, regular_reward):
        
        if regular_reward.lower() in ['yes', 'y', 'true', '1']:
            regular_reward = True
        elif regular_reward.lower() in ['no', 'n', 'false', '0']:
            regular_reward = False
        else:
            return f'Error: Invalid input for regular_reward. Please enter "yes" or "no".'
        
        new_reward = pd.DataFrame([[reward_name, reward_price, regular_reward]], columns=['reward_name', 'reward_price', 'regular_reward'])
        # Ensure the CSV file ends with a newline before appending to avoid concatenation with the last line
        try:
            with open('rewards.csv', 'rb+') as f:
                f.seek(0, 2)
                if f.tell() > 0:
                    f.seek(-1, 2)
                    last = f.read(1)
                    if last != b'\n':
                        f.write(b'\n')
        except FileNotFoundError:
            # File doesn't exist yet, to_csv will create it
            pass
        new_reward.to_csv('rewards.csv', index=False, mode='a', header=False)
        return f'Reward \"{reward_name}\" added successfully!'

# -------------Testing the classes------------------
load_data()

test_act = Activity()
test_rwd = Reward()
test_mgr = Manager()
test_acv = Achievement()

user1 = User(df_users.iloc[0, 0], df_users.iloc[0, 1], df_users.iloc[0, 2], df_users.iloc[0, 3])

while True:
    print('\n\nAvailable Actions: ')
    lst_act = ['Quit', 'Show Activities', 'Show Rewards', 'Show Status','Complete Activity', 'Redeem Reward', 'Add Activity', 'Add Reward', 'Show Achivements']
    for i in range(len(lst_act)):
        print(f'{i}. {lst_act[i]}')

    print('\n')
    i = input('What would you like to do? Enter the number of an operation : ')
    
    match i:
        case '0':
            user1.update_user()
            break
        case '1':
            test_act.show_activities()
        case '2':
            test_rwd.show_rewards()
        case '3':
            user1.show_status()
        case '4':
            user1.complete_activity(test_act)
        case '5':
            user1.redeem_reward(test_rwd)
        case '6':
            name = input('Enter the activity name: ')
            try:
                points = int(input('Enter the activity points: '))
            except ValueError:
                print('Error: Activity points must be an integer.')
                continue
            is_daily = input('Is this a daily task? (yes/no): ')
            result = test_mgr.add_activity(name, points, is_daily)
            print(result)
        case '7':
            name = input('Enter the reward name: ')
            try:
                price = int(input('Enter the reward price: '))
            except ValueError:
                print('Error: Reward price must be an integer.')
                continue
            regular = input('Is this a regular reward? (yes/no): ')
            
            result = test_mgr.add_reward(name, price, regular)
            print(result)
        case '8':
            test_acv.show_achievements()
        case _:
            print(f'{i} is invalid operation number!')
            