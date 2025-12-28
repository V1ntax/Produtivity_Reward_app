import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd

class RewardsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rewards & Activities Tracker")
        self.root.geometry("950x800")
        
        # Dark theme colors
        self.bg_dark = '#1e1e2e'
        self.bg_darker = '#181825'
        self.bg_card = '#282839'
        self.accent_purple = '#b4befe'
        self.accent_blue = '#89b4fa'
        self.accent_green = '#a6e3a1'
        self.accent_red = '#f38ba8'
        self.accent_yellow = '#f9e2af'
        self.text_primary = '#cdd6f4'
        self.text_secondary = '#a6adc8'
        
        self.root.configure(bg=self.bg_dark)
        
        # Achievement emojis mapping
        self.achievement_emojis = {
            'Beginner': '🌱',
            'Novice': '⭐',
            'Intermediate': '🔥',
            'Professional': '💎',
            'Expert': '👑',
            'Master': '🏆',
            'Grandmaster': '🎖️',
            'Legend': '⚡',
            'Mythic': '🌟',
            'Enlightened': '✨'
        }
        
        # Setup auto-save on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Load data
        self.load_data()
        
        # Initialize current user
        self.current_user = None
        self.current_user_index = 0
        if not self.df_users.empty:
            self.load_user(0)
        
        # Create GUI
        self.create_widgets()
        self.update_display()
    
    def load_data(self):
        """Load all CSV data"""
        try:
            self.df_users = pd.read_csv('users.csv')
            self.df_activities = pd.read_csv('activities.csv')
            self.df_rewards = pd.read_csv('rewards.csv')
            self.df_achievements = pd.read_csv('achievements.csv')
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Required CSV file not found: {e}")
            self.root.destroy()
    
    def reload_data(self):
        """Reload data from CSV files"""
        self.load_data()
        self.populate_activities()
        self.populate_rewards()
        self.update_display()
    
    def load_user(self, index):
        """Load user data from dataframe"""
        if index < len(self.df_users):
            row = self.df_users.iloc[index]
            self.current_user_index = index
            self.current_user = {
                'name': row['name'],
                'total_points': int(row['total_points']),
                'activities_completed': int(row['activities_completed']),
                'alltime_points': int(row['alltime_points'])
            }
    
    def save_user(self):
        """Save current user data back to CSV"""
        mask = self.df_users['name'] == self.current_user['name']
        self.df_users.loc[mask, 'total_points'] = self.current_user['total_points']
        self.df_users.loc[mask, 'activities_completed'] = self.current_user['activities_completed']
        self.df_users.loc[mask, 'alltime_points'] = self.current_user['alltime_points']
        self.df_users.to_csv('users.csv', index=False)
    
    def add_activity_to_csv(self, activity_name, activity_points, is_daily):
        """Add new activity to CSV"""
        df = pd.read_csv('activities.csv')
        new_activity = pd.DataFrame([[activity_name, activity_points, is_daily]], 
                                    columns=['activity_name', 'activity_points', 'daily_task'])
        df = pd.concat([df, new_activity], ignore_index=True)
        df.to_csv('activities.csv', index=False)
    
    def add_reward_to_csv(self, reward_name, reward_price, is_regular):
        """Add new reward to CSV"""
        df = pd.read_csv('rewards.csv')
        new_reward = pd.DataFrame([[reward_name, reward_price, is_regular]], 
                                  columns=['reward_name', 'reward_price', 'regular_reward'])
        df = pd.concat([df, new_reward], ignore_index=True)
        df.to_csv('rewards.csv', index=False)
    
    def add_user_to_csv(self, name):
        """Add new user to CSV"""
        df = pd.read_csv('users.csv')
        new_user = pd.DataFrame([[name, 0, 0, 0]], 
                               columns=['name', 'total_points', 'activities_completed', 'alltime_points'])
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_csv('users.csv', index=False)
    
    def delete_user_from_csv(self, user_name):
        """Delete user from CSV"""
        self.df_users = self.df_users[self.df_users['name'] != user_name]
        self.df_users.to_csv('users.csv', index=False)
    
    def define_rank(self):
        """Calculate user's current achievement rank based on alltime_points"""
        if not self.current_user:
            return "Beginner"
        
        alltime_pts = self.current_user['alltime_points']
        tasks = self.current_user['activities_completed']
        
        current_rank = self.df_achievements.iloc[0]['achievement_name']
        
        for idx, row in self.df_achievements.iterrows():
            if alltime_pts >= row['points_required'] or tasks >= row['tasks_required']:
                current_rank = row['achievement_name']
            else:
                break
        
        return current_rank
    
    def create_widgets(self):
        # Header with fancy styling
        header_frame = tk.Frame(self.root, bg=self.bg_darker, height=90)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Title with cyberpunk feel
        title_container = tk.Frame(header_frame, bg=self.bg_darker)
        title_container.place(relx=0.5, rely=0.5, anchor='center')
        
        title_label = tk.Label(title_container, text="⚡ REWARDS TRACKER", 
                              font=('Consolas', 28, 'bold'), 
                              bg=self.bg_darker, fg=self.accent_blue)
        title_label.pack()
        
        subtitle_label = tk.Label(title_container, text="// Achievement System v2.0", 
                                 font=('Consolas', 10), 
                                 bg=self.bg_darker, fg=self.text_secondary)
        subtitle_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_dark)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - User Status
        left_panel = tk.Frame(main_container, bg=self.bg_card, relief='flat', bd=0)
        left_panel.pack(side='left', fill='both', padx=(0, 15), pady=5)
        
        # User status section with border effect
        status_border = tk.Frame(left_panel, bg=self.accent_blue, height=3)
        status_border.pack(fill='x')
        
        status_header = tk.Label(left_panel, text="┌─ USER STATUS ─┐", 
                                font=('Consolas', 13, 'bold'), 
                                bg=self.bg_card, fg=self.accent_blue, pady=15)
        status_header.pack(fill='x')
        
        status_content = tk.Frame(left_panel, bg=self.bg_card)
        status_content.pack(fill='both', expand=True, padx=25, pady=20)
        
        # User selection button
        user_select_btn = tk.Button(status_content, text="🔄 SWITCH USER", 
                                    command=self.show_user_menu,
                                    font=('Consolas', 9, 'bold'),
                                    bg=self.accent_blue, fg=self.bg_darker,
                                    activebackground=self.accent_purple,
                                    activeforeground=self.bg_darker,
                                    padx=15, pady=8,
                                    relief='flat',
                                    cursor='hand2',
                                    borderwidth=0)
        user_select_btn.pack(pady=(0, 15))
        
        # User icon and name
        user_frame = tk.Frame(status_content, bg=self.bg_darker, relief='flat')
        user_frame.pack(fill='x', pady=(0, 20), ipady=15)
        
        icon_label = tk.Label(user_frame, text="👤", 
                             font=('Arial', 24), 
                             bg=self.bg_darker)
        icon_label.pack(pady=(10, 5))
        
        self.name_label = tk.Label(user_frame, text="", 
                                   font=('Consolas', 13, 'bold'), 
                                   bg=self.bg_darker, fg=self.accent_purple)
        self.name_label.pack(pady=(0, 10))
        
        # Points display with fancy box
        points_frame = tk.Frame(status_content, bg=self.bg_darker, relief='flat')
        points_frame.pack(fill='x', pady=10, ipady=15)
        
        points_title = tk.Label(points_frame, text="// CURRENT POINTS", 
                               font=('Consolas', 9), 
                               bg=self.bg_darker, fg=self.text_secondary)
        points_title.pack(pady=(10, 5))
        
        self.points_label = tk.Label(points_frame, text="", 
                                     font=('Consolas', 22, 'bold'), 
                                     bg=self.bg_darker, fg=self.accent_green)
        self.points_label.pack()
        
        # All-time points display
        alltime_frame = tk.Frame(status_content, bg=self.bg_darker, relief='flat')
        alltime_frame.pack(fill='x', pady=10, ipady=12)
        
        alltime_title = tk.Label(alltime_frame, text="// ALL-TIME POINTS", 
                                font=('Consolas', 9), 
                                bg=self.bg_darker, fg=self.text_secondary)
        alltime_title.pack(pady=(8, 3))
        
        self.alltime_label = tk.Label(alltime_frame, text="", 
                                      font=('Consolas', 16, 'bold'), 
                                      bg=self.bg_darker, fg=self.accent_yellow)
        self.alltime_label.pack()
        
        # Activities completed
        activities_frame = tk.Frame(status_content, bg=self.bg_darker, relief='flat')
        activities_frame.pack(fill='x', pady=10, ipady=12)
        
        self.activities_label = tk.Label(activities_frame, text="", 
                                         font=('Consolas', 10), 
                                         bg=self.bg_darker, fg=self.text_primary)
        self.activities_label.pack(pady=8)
        
        # Achievement rank display
        rank_frame = tk.Frame(status_content, bg=self.bg_darker, relief='flat')
        rank_frame.pack(fill='x', pady=10, ipady=12)
        
        rank_title = tk.Label(rank_frame, text="// CURRENT RANK", 
                             font=('Consolas', 9), 
                             bg=self.bg_darker, fg=self.text_secondary)
        rank_title.pack(pady=(8, 5))
        
        self.rank_label = tk.Label(rank_frame, text="", 
                                   font=('Consolas', 14, 'bold'), 
                                   bg=self.bg_darker, fg=self.accent_yellow)
        self.rank_label.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(status_content, bg=self.bg_card)
        buttons_frame.pack(fill='x', pady=(15, 0))
        
        # View achievements button
        achievements_btn = tk.Button(buttons_frame, text="🏆 VIEW ACHIEVEMENTS", 
                                    command=self.show_achievements,
                                    font=('Consolas', 9, 'bold'),
                                    bg=self.accent_yellow, fg=self.bg_darker,
                                    activebackground=self.accent_purple,
                                    activeforeground=self.bg_darker,
                                    padx=15, pady=8,
                                    relief='flat',
                                    cursor='hand2',
                                    borderwidth=0)
        achievements_btn.pack(fill='x', pady=(0, 8))
        
        # Save button with hover effect
        save_btn = tk.Button(buttons_frame, text="⚡ SAVE PROGRESS", 
                           command=self.handle_save,
                           font=('Consolas', 10, 'bold'),
                           bg=self.accent_green, fg=self.bg_darker,
                           activebackground=self.accent_blue,
                           activeforeground=self.bg_darker,
                           padx=20, pady=10,
                           relief='flat',
                           cursor='hand2',
                           borderwidth=0)
        save_btn.pack(fill='x')
        
        # Right panel - Activities and Rewards
        right_panel = tk.Frame(main_container, bg=self.bg_dark)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Activities section
        activities_section = tk.Frame(right_panel, bg=self.bg_card, relief='flat')
        activities_section.pack(fill='both', expand=True, pady=(0, 15))
        
        act_border = tk.Frame(activities_section, bg=self.accent_purple, height=3)
        act_border.pack(fill='x')
        
        # Activity header with add button
        act_header_frame = tk.Frame(activities_section, bg=self.bg_card)
        act_header_frame.pack(fill='x')
        
        act_header = tk.Label(act_header_frame, text="┌─ COMPLETE ACTIVITY ─┐", 
                             font=('Consolas', 12, 'bold'), 
                             bg=self.bg_card, fg=self.accent_purple, pady=12)
        act_header.pack(side='left', padx=(10, 0))
        
        # Activity management buttons
        act_btn_frame = tk.Frame(act_header_frame, bg=self.bg_card)
        act_btn_frame.pack(side='right', padx=10)
        
        add_act_btn = tk.Button(act_btn_frame, text="+ ADD", 
                               command=self.add_activity_dialog,
                               font=('Consolas', 8, 'bold'),
                               bg=self.accent_green, fg=self.bg_darker,
                               padx=8, pady=5,
                               relief='flat',
                               cursor='hand2',
                               borderwidth=0)
        add_act_btn.pack(side='left', padx=2)
        
        edit_act_btn = tk.Button(act_btn_frame, text="✎ EDIT", 
                                command=self.edit_activity_dialog,
                                font=('Consolas', 8, 'bold'),
                                bg=self.accent_blue, fg=self.bg_darker,
                                padx=8, pady=5,
                                relief='flat',
                                cursor='hand2',
                                borderwidth=0)
        edit_act_btn.pack(side='left', padx=2)
        
        del_act_btn = tk.Button(act_btn_frame, text="✗ DEL", 
                               command=self.delete_activity,
                               font=('Consolas', 8, 'bold'),
                               bg=self.accent_red, fg=self.bg_darker,
                               padx=8, pady=5,
                               relief='flat',
                               cursor='hand2',
                               borderwidth=0)
        del_act_btn.pack(side='left', padx=2)
        
        # Activities listbox
        act_list_frame = tk.Frame(activities_section, bg=self.bg_card)
        act_list_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        act_scrollbar = tk.Scrollbar(act_list_frame, bg=self.bg_darker, 
                                     troughcolor=self.bg_darker,
                                     activebackground=self.accent_purple)
        act_scrollbar.pack(side='right', fill='y')
        
        self.activities_listbox = tk.Listbox(act_list_frame, 
                                            font=('Consolas', 10),
                                            yscrollcommand=act_scrollbar.set,
                                            selectmode='single',
                                            bg=self.bg_darker,
                                            fg=self.text_primary,
                                            selectbackground=self.accent_purple,
                                            selectforeground=self.bg_darker,
                                            relief='flat',
                                            bd=0,
                                            highlightthickness=0,
                                            activestyle='none')
        self.activities_listbox.pack(side='left', fill='both', expand=True)
        act_scrollbar.config(command=self.activities_listbox.yview)
        
        complete_btn = tk.Button(activities_section, text=">> EXECUTE ACTIVITY", 
                               command=self.complete_activity,
                               font=('Consolas', 10, 'bold'),
                               bg=self.accent_purple, fg=self.bg_darker,
                               activebackground=self.accent_blue,
                               activeforeground=self.bg_darker,
                               padx=20, pady=10,
                               relief='flat',
                               cursor='hand2',
                               borderwidth=0)
        complete_btn.pack(pady=15)
        # Rewards section
        rewards_section = tk.Frame(right_panel, bg=self.bg_card, relief='flat')
        rewards_section.pack(fill='both', expand=True)
        
        rwd_border = tk.Frame(rewards_section, bg=self.accent_red, height=3)
        rwd_border.pack(fill='x')
        
        # Reward header with add button
        rwd_header_frame = tk.Frame(rewards_section, bg=self.bg_card)
        rwd_header_frame.pack(fill='x')
        
        rwd_header = tk.Label(rwd_header_frame, text="┌─ REDEEM REWARD ─┐", 
                            font=('Consolas', 12, 'bold'), 
                            bg=self.bg_card, fg=self.accent_red, pady=12)
        rwd_header.pack(side='left', padx=(10, 0))
        
        # Reward management buttons
        rwd_btn_frame = tk.Frame(rwd_header_frame, bg=self.bg_card)
        rwd_btn_frame.pack(side='right', padx=10)
        
        add_rwd_btn = tk.Button(rwd_btn_frame, text="+ ADD", 
                               command=self.add_reward_dialog,
                               font=('Consolas', 8, 'bold'),
                               bg=self.accent_green, fg=self.bg_darker,
                               padx=8, pady=5,
                               relief='flat',
                               cursor='hand2',
                               borderwidth=0)
        add_rwd_btn.pack(side='left', padx=2)
        
        edit_rwd_btn = tk.Button(rwd_btn_frame, text="✎ EDIT", 
                                command=self.edit_reward_dialog,
                                font=('Consolas', 8, 'bold'),
                                bg=self.accent_blue, fg=self.bg_darker,
                                padx=8, pady=5,
                                relief='flat',
                                cursor='hand2',
                                borderwidth=0)
        edit_rwd_btn.pack(side='left', padx=2)
        
        del_rwd_btn = tk.Button(rwd_btn_frame, text="✗ DEL", 
                               command=self.delete_reward,
                               font=('Consolas', 8, 'bold'),
                               bg=self.accent_red, fg=self.bg_darker,
                               padx=8, pady=5,
                               relief='flat',
                               cursor='hand2',
                               borderwidth=0)
        del_rwd_btn.pack(side='left', padx=2)
        
        # Rewards listbox
        rwd_list_frame = tk.Frame(rewards_section, bg=self.bg_card)
        rwd_list_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        rwd_scrollbar = tk.Scrollbar(rwd_list_frame, bg=self.bg_darker,
                                     troughcolor=self.bg_darker,
                                     activebackground=self.accent_red)
        rwd_scrollbar.pack(side='right', fill='y')
        
        self.rewards_listbox = tk.Listbox(rwd_list_frame, 
                                         font=('Consolas', 10),
                                         yscrollcommand=rwd_scrollbar.set,
                                         selectmode='single',
                                         bg=self.bg_darker,
                                         fg=self.text_primary,
                                         selectbackground=self.accent_red,
                                         selectforeground=self.bg_darker,
                                         relief='flat',
                                         bd=0,
                                         highlightthickness=0,
                                         activestyle='none')
        self.rewards_listbox.pack(side='left', fill='both', expand=True)
        rwd_scrollbar.config(command=self.rewards_listbox.yview)
        
        redeem_btn = tk.Button(rewards_section, text=">> CLAIM REWARD", 
                             command=self.redeem_reward,
                             font=('Consolas', 10, 'bold'),
                             bg=self.accent_red, fg=self.bg_darker,
                             activebackground=self.accent_yellow,
                             activeforeground=self.bg_darker,
                             padx=20, pady=10,
                             relief='flat',
                             cursor='hand2',
                             borderwidth=0)
        redeem_btn.pack(pady=15)
        
        # Footer
        footer = tk.Label(self.root, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
                         font=('Consolas', 8), 
                         bg=self.bg_dark, fg=self.text_secondary)
        footer.pack(side='bottom', pady=(10, 5))
        
        # Populate listboxes
        self.populate_activities()
        self.populate_rewards()
    
    def populate_activities(self):
        """Fill activities listbox sorted by category and points"""
        self.activities_listbox.delete(0, tk.END)
        
        # Separate daily and misc activities
        daily_arr = []
        misc_arr = []
        
        for idx, row in self.df_activities.iterrows():
            name = row['activity_name']
            points = int(row['activity_points'])
            is_daily = row['daily_task']
            
            if is_daily:
                daily_arr.append((idx, name, points))
            else:
                misc_arr.append((idx, name, points))
        
        # Sort by points
        daily_arr_sorted = sorted(daily_arr, key=lambda x: x[2])
        misc_arr_sorted = sorted(misc_arr, key=lambda x: x[2])
        
        # Display daily tasks header
        if daily_arr_sorted:
            self.activities_listbox.insert(tk.END, "═══ DAILY TASKS ═══")
            self.activities_listbox.itemconfig(tk.END, {'bg': self.accent_purple, 'fg': self.bg_darker})
            
            for idx, name, points in daily_arr_sorted:
                self.activities_listbox.insert(tk.END, f"├─ {name} [+{points} pts]")
        
        # Display miscellaneous header
        if misc_arr_sorted:
            if daily_arr_sorted:
                self.activities_listbox.insert(tk.END, "")  # Spacer
            self.activities_listbox.insert(tk.END, "═══ MISCELLANEOUS ═══")
            self.activities_listbox.itemconfig(tk.END, {'bg': self.accent_blue, 'fg': self.bg_darker})
            
            for idx, name, points in misc_arr_sorted:
                self.activities_listbox.insert(tk.END, f"├─ {name} [+{points} pts]")
    
    def populate_rewards(self):
        """Fill rewards listbox sorted by category and price"""
        self.rewards_listbox.delete(0, tk.END)
        
        # Separate regular and long-term rewards
        regular_arr = []
        longterm_arr = []
        
        for idx, row in self.df_rewards.iterrows():
            name = row['reward_name']
            price = int(row['reward_price'])
            is_regular = row['regular_reward']
            
            if is_regular:
                regular_arr.append((idx, name, price))
            else:
                longterm_arr.append((idx, name, price))
        
        # Sort by price
        regular_arr_sorted = sorted(regular_arr, key=lambda x: x[2])
        longterm_arr_sorted = sorted(longterm_arr, key=lambda x: x[2])
        
        # Display regular rewards header
        if regular_arr_sorted:
            self.rewards_listbox.insert(tk.END, "═══ REGULAR REWARDS ═══")
            self.rewards_listbox.itemconfig(tk.END, {'bg': self.accent_red, 'fg': self.bg_darker})
            
            for idx, name, price in regular_arr_sorted:
                self.rewards_listbox.insert(tk.END, f"├─ {name} [{price} pts]")
        
        # Display long-term rewards header
        if longterm_arr_sorted:
            if regular_arr_sorted:
                self.rewards_listbox.insert(tk.END, "")  # Spacer
            self.rewards_listbox.insert(tk.END, "═══ LONG-TERM REWARDS ═══")
            self.rewards_listbox.itemconfig(tk.END, {'bg': self.accent_yellow, 'fg': self.bg_darker})
            
            for idx, name, price in longterm_arr_sorted:
                self.rewards_listbox.insert(tk.END, f"├─ {name} [{price} pts]")
    
    def get_selected_activity_index(self):
        """Get the actual dataframe index of selected activity"""
        selection = self.activities_listbox.curselection()
        if not selection:
            return None
        
        selected_idx = selection[0]
        selected_text = self.activities_listbox.get(selected_idx)
        
        # Skip headers and spacers
        if "═══" in selected_text or selected_text.strip() == "":
            return None
        
        # Extract activity name
        if "├─" in selected_text:
            activity_name = selected_text.split("├─")[1].split("[")[0].strip()
            # Find in dataframe
            for idx, row in self.df_activities.iterrows():
                if row['activity_name'] == activity_name:
                    return idx
        return None
    
    def get_selected_reward_index(self):
        """Get the actual dataframe index of selected reward"""
        selection = self.rewards_listbox.curselection()
        if not selection:
            return None
        
        selected_idx = selection[0]
        selected_text = self.rewards_listbox.get(selected_idx)
        
        # Skip headers and spacers
        if "═══" in selected_text or selected_text.strip() == "":
            return None
        
        # Extract reward name
        if "├─" in selected_text:
            reward_name = selected_text.split("├─")[1].split("[")[0].strip()
            # Find in dataframe
            for idx, row in self.df_rewards.iterrows():
                if row['reward_name'] == reward_name:
                    return idx
        return None
    
    def update_display(self):
        """Update user status display"""
        if self.current_user:
            self.name_label.config(text=f"// {self.current_user['name'].upper()}")
            self.points_label.config(text=f"{self.current_user['total_points']} ⚡")
            self.alltime_label.config(text=f"{self.current_user['alltime_points']} ✨")
            self.activities_label.config(
                text=f"├─ Completed: {self.current_user['activities_completed']} tasks")
            
            # Update rank display
            current_rank = self.define_rank()
            emoji = self.achievement_emojis.get(current_rank, '🎯')
            self.rank_label.config(text=f"{emoji} {current_rank.upper()}")
    
    def show_achievements(self):
        """Show achievements window"""
        achievements_window = tk.Toplevel(self.root)
        achievements_window.title("Achievements")
        achievements_window.geometry("600x700")
        achievements_window.configure(bg=self.bg_dark)
        
        # Header
        header = tk.Label(achievements_window, text="🏆 ACHIEVEMENT RANKS", 
                         font=('Consolas', 18, 'bold'),
                         bg=self.bg_darker, fg=self.accent_yellow, pady=20)
        header.pack(fill='x')
        
        # Current rank info
        current_rank = self.define_rank()
        emoji = self.achievement_emojis.get(current_rank, '🎯')
        
        current_frame = tk.Frame(achievements_window, bg=self.bg_card, relief='flat')
        current_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        current_label = tk.Label(current_frame, 
                                text=f"YOUR CURRENT RANK: {emoji} {current_rank.upper()}", 
                                font=('Consolas', 14, 'bold'),
                                bg=self.bg_card, fg=self.accent_green, pady=15)
        current_label.pack()
        
        # Progress info
        progress_text = f"├─ All-time: {self.current_user['alltime_points']} pts  |  Tasks: {self.current_user['activities_completed']} ✓"
        progress_label = tk.Label(current_frame, text=progress_text,
                                 font=('Consolas', 10),
                                 bg=self.bg_card, fg=self.text_secondary, pady=(0, 10))
        progress_label.pack()
        
        # Direct frame approach - NO CANVAS
        achievements_container = tk.Frame(achievements_window, bg=self.bg_card)
        achievements_container.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Add all achievements directly
        for idx in range(len(self.df_achievements)):
            row = self.df_achievements.iloc[idx]
            rank_name = str(row['achievement_name']).strip()
            points_req = int(row['points_required'])
            tasks_req = int(row['tasks_required'])
            emoji_char = self.achievement_emojis.get(rank_name, '🎯')
            
            # Check if achieved
            is_achieved = (self.current_user['alltime_points'] >= points_req or 
                          self.current_user['activities_completed'] >= tasks_req)
            is_current = (rank_name == current_rank)
            
            # Achievement card colors
            if is_current:
                card_bg = self.accent_green
                text_color = self.bg_darker
            elif is_achieved:
                card_bg = self.bg_darker
                text_color = self.accent_green
            else:
                card_bg = self.bg_darker
                text_color = self.text_secondary
            
            # Create card - DIRECTLY in container
            card = tk.Frame(achievements_container, bg=card_bg, relief='solid', bd=1)
            card.pack(fill='x', padx=10, pady=5, ipady=8)
            
            # Rank name with emoji
            rank_header = tk.Label(card, 
                                  text=f"{emoji_char} {rank_name.upper()}",
                                  font=('Consolas', 11, 'bold'),
                                  bg=card_bg, fg=text_color,
                                  anchor='w')
            rank_header.pack(fill='x', padx=12, pady=(6, 3))
            
            # Requirements
            req_text = f"└─ Requires: {points_req} pts OR {tasks_req} tasks"
            req_label = tk.Label(card, text=req_text,
                               font=('Consolas', 9),
                               bg=card_bg, fg=text_color,
                               anchor='w')
            req_label.pack(fill='x', padx=12, pady=(0, 3))
            
            # Status
            if is_current:
                status_text = ">>> CURRENT RANK <<<"
            elif is_achieved:
                status_text = "✓ ACHIEVED"
            else:
                status_text = "🔒 LOCKED"
            
            status_label = tk.Label(card, text=status_text,
                                  font=('Consolas', 8, 'bold'),
                                  bg=card_bg, fg=text_color,
                                  anchor='w')
            status_label.pack(fill='x', padx=12, pady=(0, 6))
        
        # Close button
        close_btn = tk.Button(achievements_window, text=">> CLOSE",
                            command=achievements_window.destroy,
                            font=('Consolas', 10, 'bold'),
                            bg=self.accent_blue, fg=self.bg_darker,
                            padx=20, pady=10,
                            relief='flat',
                            cursor='hand2')
        close_btn.pack(pady=15)
    
    def show_user_menu(self):
        """Show user management menu"""
        menu_window = tk.Toplevel(self.root)
        menu_window.title("User Management")
        menu_window.geometry("400x500")
        menu_window.configure(bg=self.bg_dark)
        menu_window.transient(self.root)
        menu_window.grab_set()
        
        # Header
        header = tk.Label(menu_window, text="👥 USER MANAGEMENT", 
                         font=('Consolas', 16, 'bold'),
                         bg=self.bg_darker, fg=self.accent_blue, pady=15)
        header.pack(fill='x')
        
        # Users listbox
        list_frame = tk.Frame(menu_window, bg=self.bg_card)
        list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        scrollbar = tk.Scrollbar(list_frame, bg=self.bg_darker)
        scrollbar.pack(side='right', fill='y')
        
        users_listbox = tk.Listbox(list_frame,
                                   font=('Consolas', 11),
                                   yscrollcommand=scrollbar.set,
                                   bg=self.bg_darker,
                                   fg=self.text_primary,
                                   selectbackground=self.accent_blue,
                                   selectforeground=self.bg_darker,
                                   relief='flat',
                                   bd=0,
                                   highlightthickness=0)
        users_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=users_listbox.yview)
        
        # Populate users
        self.reload_data()
        for idx, row in self.df_users.iterrows():
            users_listbox.insert(tk.END, f"├─ {row['name']} ({row['alltime_points']} all-time pts)")
        
        # Select current user
        if self.current_user_index < users_listbox.size():
            users_listbox.selection_set(self.current_user_index)
        
        # Buttons frame
        btn_frame = tk.Frame(menu_window, bg=self.bg_dark)
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        def select_user():
            selection = users_listbox.curselection()
            if selection:
                self.save_user()
                self.load_user(selection[0])
                self.update_display()
                menu_window.destroy()
        
        def add_user():
            name = simpledialog.askstring("Add User", "Enter user name:", parent=menu_window)
            if name:
                self.add_user_to_csv(name)
                self.reload_data()
                users_listbox.delete(0, tk.END)
                for idx, row in self.df_users.iterrows():
                    users_listbox.insert(tk.END, f"├─ {row['name']} ({row['alltime_points']} all-time pts)")
                messagebox.showinfo("Success", f"User '{name}' added!", parent=menu_window)
        
        def delete_user():
            selection = users_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a user to delete!", parent=menu_window)
                return
            
            user_name = self.df_users.iloc[selection[0]]['name']
            
            if len(self.df_users) <= 1:
                messagebox.showerror("Error", "Cannot delete the last user!", parent=menu_window)
                return
            
            confirm = messagebox.askyesno("Confirm Delete", 
                                         f"Delete user '{user_name}'?\nThis cannot be undone!", 
                                         parent=menu_window)
            if confirm:
                self.delete_user_from_csv(user_name)
                self.reload_data()
                users_listbox.delete(0, tk.END)
                for idx, row in self.df_users.iterrows():
                    users_listbox.insert(tk.END, f"├─ {row['name']} ({row['alltime_points']} all-time pts)")
                
                if self.current_user['name'] == user_name:
                    self.load_user(0)
                    self.update_display()
                
                messagebox.showinfo("Deleted", f"User '{user_name}' deleted!", parent=menu_window)
        
        select_btn = tk.Button(btn_frame, text=">> SELECT USER",
                              command=select_user,
                              font=('Consolas', 10, 'bold'),
                              bg=self.accent_blue, fg=self.bg_darker,
                              padx=15, pady=10,
                              relief='flat',
                              cursor='hand2')
        select_btn.pack(side='top', fill='x', pady=(0, 10))
        
        add_btn = tk.Button(btn_frame, text="+ ADD USER",
                           command=add_user,
                           font=('Consolas', 10, 'bold'),
                           bg=self.accent_green, fg=self.bg_darker,
                           padx=15, pady=10,
                           relief='flat',
                           cursor='hand2')
        add_btn.pack(side='top', fill='x', pady=(0, 10))
        
        del_btn = tk.Button(btn_frame, text="✗ DELETE USER",
                           command=delete_user,
                           font=('Consolas', 10, 'bold'),
                           bg=self.accent_red, fg=self.bg_darker,
                           padx=15, pady=10,
                           relief='flat',
                           cursor='hand2')
        del_btn.pack(side='top', fill='x')
    
    def add_activity_dialog(self):
        """Show dialog to add new activity"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Activity")
        dialog.geometry("450x350")
        dialog.configure(bg=self.bg_dark)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header = tk.Label(dialog, text="➕ ADD NEW ACTIVITY", 
                         font=('Consolas', 14, 'bold'),
                         bg=self.bg_darker, fg=self.accent_purple, pady=15)
        header.pack(fill='x')
        
        # Content
        content = tk.Frame(dialog, bg=self.bg_dark)
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(content, text="Activity Name:", font=('Consolas', 10),
                bg=self.bg_dark, fg=self.text_primary).pack(anchor='w', pady=(0, 5))
        name_entry = tk.Entry(content, font=('Consolas', 11), 
                             bg=self.bg_card, fg=self.text_primary,
                             insertbackground=self.text_primary,
                             relief='flat', bd=5)
        name_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(content, text="Points:", font=('Consolas', 10),
                bg=self.bg_dark, fg=self.text_primary).pack(anchor='w', pady=(0, 5))
        points_entry = tk.Entry(content, font=('Consolas', 11),
                               bg=self.bg_card, fg=self.text_primary,
                               insertbackground=self.text_primary,
                               relief='flat', bd=5)
        points_entry.pack(fill='x', pady=(0, 15))
        
        # Daily task checkbox
        is_daily_var = tk.BooleanVar(value=False)
        daily_check = tk.Checkbutton(content, text="Daily Task", 
                                     variable=is_daily_var,
                                     font=('Consolas', 10, 'bold'),
                                     bg=self.bg_dark, fg=self.accent_purple,
                                     selectcolor=self.bg_card,
                                     activebackground=self.bg_dark,
                                     activeforeground=self.accent_blue,
                                     cursor='hand2')
        daily_check.pack(anchor='w', pady=(0, 20))
        
        def submit():
            name = name_entry.get().strip()
            points_str = points_entry.get().strip()
            
            if not name or not points_str:
                messagebox.showwarning("Empty Fields", "Please fill all fields!", parent=dialog)
                return
            
            try:
                points = int(points_str)
                if points <= 0:
                    messagebox.showerror("Invalid Points", "Points must be positive!", parent=dialog)
                    return
            except ValueError:
                messagebox.showerror("Invalid Points", "Points must be a number!", parent=dialog)
                return
            
            self.add_activity_to_csv(name, points, is_daily_var.get())
            self.reload_data()
            messagebox.showinfo("Success", f"Activity '{name}' added!", parent=dialog)
            dialog.destroy()
        
        submit_btn = tk.Button(content, text=">> ADD ACTIVITY",
                              command=submit,
                              font=('Consolas', 10, 'bold'),
                              bg=self.accent_purple, fg=self.bg_darker,
                              padx=20, pady=10,
                              relief='flat',
                              cursor='hand2')
        submit_btn.pack(fill='x')
    
    def add_reward_dialog(self):
        """Show dialog to add new reward"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Reward")
        dialog.geometry("450x350")
        dialog.configure(bg=self.bg_dark)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header = tk.Label(dialog, text="➕ ADD NEW REWARD", 
                         font=('Consolas', 14, 'bold'),
                         bg=self.bg_darker, fg=self.accent_red, pady=15)
        header.pack(fill='x')
        
        # Content
        content = tk.Frame(dialog, bg=self.bg_dark)
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(content, text="Reward Name:", font=('Consolas', 10),
                bg=self.bg_dark, fg=self.text_primary).pack(anchor='w', pady=(0, 5))
        name_entry = tk.Entry(content, font=('Consolas', 11),
                             bg=self.bg_card, fg=self.text_primary,
                             insertbackground=self.text_primary,
                             relief='flat', bd=5)
        name_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(content, text="Price (points):", font=('Consolas', 10),
                bg=self.bg_dark, fg=self.text_primary).pack(anchor='w', pady=(0, 5))
        price_entry = tk.Entry(content, font=('Consolas', 11),
                              bg=self.bg_card, fg=self.text_primary,
                              insertbackground=self.text_primary,
                              relief='flat', bd=5)
        price_entry.pack(fill='x', pady=(0, 15))
        
        # Regular reward checkbox
        is_regular_var = tk.BooleanVar(value=True)
        regular_check = tk.Checkbutton(content, text="Regular Reward", 
                                      variable=is_regular_var,
                                      font=('Consolas', 10, 'bold'),
                                      bg=self.bg_dark, fg=self.accent_red,
                                      selectcolor=self.bg_card,
                                      activebackground=self.bg_dark,
                                      activeforeground=self.accent_yellow,
                                      cursor='hand2')
        regular_check.pack(anchor='w', pady=(0, 20))
        
        def submit():
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            
            if not name or not price_str:
                messagebox.showwarning("Empty Fields", "Please fill all fields!", parent=dialog)
                return
            
            try:
                price = int(price_str)
                if price <= 0:
                    messagebox.showerror("Invalid Price", "Price must be positive!", parent=dialog)
                    return
            except ValueError:
                messagebox.showerror("Invalid Price", "Price must be a number!", parent=dialog)
                return
            
            self.add_reward_to_csv(name, price, is_regular_var.get())
            self.reload_data()
            messagebox.showinfo("Success", f"Reward '{name}' added!", parent=dialog)
            dialog.destroy()
        
        submit_btn = tk.Button(content, text=">> ADD REWARD",
                              command=submit,
                              font=('Consolas', 10, 'bold'),
                              bg=self.accent_red, fg=self.bg_darker,
                              padx=20, pady=10,
                              relief='flat',
                              cursor='hand2')
        submit_btn.pack(fill='x')
    
    def edit_activity_dialog(self):
        """Show dialog to edit existing activity"""
        idx = self.get_selected_activity_index()
        if idx is None:
            messagebox.showwarning("No Selection", "Please select an activity to edit!")
            return
        
        old_activity = self.df_activities.iloc[idx]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Activity")
        dialog.geometry("450x350")
        dialog.configure(bg=self.bg_dark)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header = tk.Label(dialog, text="✎ EDIT ACTIVITY", 
                         font=('Consolas', 14, 'bold'),
                         bg=self.bg_darker, fg=self.accent_blue, pady=15)
        header.pack(fill='x')
        
        # Content
        content = tk.Frame(dialog, bg=self.bg_dark)
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(content, text="Activity Name:", font=('Consolas', 10),
                bg=self.bg_dark, fg=self.text_primary).pack(anchor='w', pady=(0, 5))
        name_entry = tk.Entry(content, font=('Consolas', 11), 
                             bg=self.bg_card, fg=self.text_primary,
                             insertbackground=self.text_primary,
                             relief='flat', bd=5)
        name_entry.insert(0, old_activity['activity_name'])
        name_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(content, text="Points:", font=('Consolas', 10),
                bg=self.bg_dark, fg=self.text_primary).pack(anchor='w', pady=(0, 5))
        points_entry = tk.Entry(content, font=('Consolas', 11),
                               bg=self.bg_card, fg=self.text_primary,
                               insertbackground=self.text_primary,
                               relief='flat', bd=5)
        points_entry.insert(0, str(old_activity['activity_points']))
        points_entry.pack(fill='x', pady=(0, 15))
        
        # Daily task checkbox
        is_daily_var = tk.BooleanVar(value=bool(old_activity['daily_task']))
        daily_check = tk.Checkbutton(content, text="Daily Task", 
                                     variable=is_daily_var,
                                     font=('Consolas', 10, 'bold'),
                                     bg=self.bg_dark, fg=self.accent_purple,
                                     selectcolor=self.bg_card,
                                     activebackground=self.bg_dark,
                                     activeforeground=self.accent_blue,
                                     cursor='hand2')
        daily_check.pack(anchor='w', pady=(0, 20))
        
        def submit():
            name = name_entry.get().strip()
            points_str = points_entry.get().strip()
            
            if not name or not points_str:
                messagebox.showwarning("Empty Fields", "Please fill all fields!", parent=dialog)
                return
            
            try:
                points = int(points_str)
                if points <= 0:
                    messagebox.showerror("Invalid Points", "Points must be positive!", parent=dialog)
                    return
            except ValueError:
                messagebox.showerror("Invalid Points", "Points must be a number!", parent=dialog)
                return
            
            # Update the activity
            self.df_activities.at[idx, 'activity_name'] = name
            self.df_activities.at[idx, 'activity_points'] = points
            self.df_activities.at[idx, 'daily_task'] = is_daily_var.get()
            self.df_activities.to_csv('activities.csv', index=False)
            self.reload_data()
            messagebox.showinfo("Success", f"Activity updated!", parent=dialog)
            dialog.destroy()
        
        submit_btn = tk.Button(content, text=">> UPDATE ACTIVITY",
                              command=submit,
                              font=('Consolas', 10, 'bold'),
                              bg=self.accent_blue, fg=self.bg_darker,
                              padx=20, pady=10,
                              relief='flat',
                              cursor='hand2')
        submit_btn.pack(fill='x')
    
    def edit_reward_dialog(self):
        """Show dialog to edit existing reward"""
        idx = self.get_selected_reward_index()
        if idx is None:
            messagebox.showwarning("No Selection", "Please select a reward to edit!")
            return
        
        old_reward = self.df_rewards.iloc[idx]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Reward")
        dialog.geometry("450x350")
        dialog.configure(bg=self.bg_dark)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header = tk.Label(dialog, text="✎ EDIT REWARD", 
                         font=('Consolas', 14, 'bold'),
                         bg=self.bg_darker, fg=self.accent_blue, pady=15)
        header.pack(fill='x')
        
        # Content
        content = tk.Frame(dialog, bg=self.bg_dark)
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(content, text="Reward Name:", font=('Consolas', 10),
                bg=self.bg_dark, fg=self.text_primary).pack(anchor='w', pady=(0, 5))
        name_entry = tk.Entry(content, font=('Consolas', 11),
                             bg=self.bg_card, fg=self.text_primary,
                             insertbackground=self.text_primary,
                             relief='flat', bd=5)
        name_entry.insert(0, old_reward['reward_name'])
        name_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(content, text="Price (points):", font=('Consolas', 10),
                bg=self.bg_dark, fg=self.text_primary).pack(anchor='w', pady=(0, 5))
        price_entry = tk.Entry(content, font=('Consolas', 11),
                              bg=self.bg_card, fg=self.text_primary,
                              insertbackground=self.text_primary,
                              relief='flat', bd=5)
        price_entry.insert(0, str(old_reward['reward_price']))
        price_entry.pack(fill='x', pady=(0, 15))
        
        # Regular reward checkbox
        is_regular_var = tk.BooleanVar(value=bool(old_reward['regular_reward']))
        regular_check = tk.Checkbutton(content, text="Regular Reward", 
                                      variable=is_regular_var,
                                      font=('Consolas', 10, 'bold'),
                                      bg=self.bg_dark, fg=self.accent_red,
                                      selectcolor=self.bg_card,
                                      activebackground=self.bg_dark,
                                      activeforeground=self.accent_yellow,
                                      cursor='hand2')
        regular_check.pack(anchor='w', pady=(0, 20))
        
        def submit():
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            
            if not name or not price_str:
                messagebox.showwarning("Empty Fields", "Please fill all fields!", parent=dialog)
                return
            
            try:
                price = int(price_str)
                if price <= 0:
                    messagebox.showerror("Invalid Price", "Price must be positive!", parent=dialog)
                    return
            except ValueError:
                messagebox.showerror("Invalid Price", "Price must be a number!", parent=dialog)
                return
            
            # Update the reward
            self.df_rewards.at[idx, 'reward_name'] = name
            self.df_rewards.at[idx, 'reward_price'] = price
            self.df_rewards.at[idx, 'regular_reward'] = is_regular_var.get()
            self.df_rewards.to_csv('rewards.csv', index=False)
            self.reload_data()
            messagebox.showinfo("Success", f"Reward updated!", parent=dialog)
            dialog.destroy()
        
        submit_btn = tk.Button(content, text=">> UPDATE REWARD",
                              command=submit,
                              font=('Consolas', 10, 'bold'),
                              bg=self.accent_blue, fg=self.bg_darker,
                              padx=20, pady=10,
                              relief='flat',
                              cursor='hand2')
        submit_btn.pack(fill='x')
    
    def delete_activity(self):
        """Delete selected activity"""
        idx = self.get_selected_activity_index()
        if idx is None:
            messagebox.showwarning("No Selection", "Please select an activity to delete!")
            return
        
        activity = self.df_activities.iloc[idx]
        
        confirm = messagebox.askyesno("Confirm Delete",
                                     f"Delete activity '{activity['activity_name']}'?\n"
                                     f"This cannot be undone!")
        
        if confirm:
            self.df_activities = self.df_activities.drop(self.df_activities.index[idx])
            self.df_activities.to_csv('activities.csv', index=False)
            self.reload_data()
            messagebox.showinfo("Deleted", f"Activity '{activity['activity_name']}' deleted!")
    
    def delete_reward(self):
        """Delete selected reward"""
        idx = self.get_selected_reward_index()
        if idx is None:
            messagebox.showwarning("No Selection", "Please select a reward to delete!")
            return
        
        reward = self.df_rewards.iloc[idx]
        
        confirm = messagebox.askyesno("Confirm Delete",
                                     f"Delete reward '{reward['reward_name']}'?\n"
                                     f"This cannot be undone!")
        
        if confirm:
            self.df_rewards = self.df_rewards.drop(self.df_rewards.index[idx])
            self.df_rewards.to_csv('rewards.csv', index=False)
            self.reload_data()
            messagebox.showinfo("Deleted", f"Reward '{reward['reward_name']}' deleted!")
    
    def complete_activity(self):
        """Handle activity completion"""
        idx = self.get_selected_activity_index()
        if idx is None:
            messagebox.showwarning("⚠ No Selection", "Please select an activity to complete!")
            return
        
        activity = self.df_activities.iloc[idx]
        old_rank = self.define_rank()
        
        self.current_user['total_points'] += int(activity['activity_points'])
        self.current_user['alltime_points'] += int(activity['activity_points'])
        self.current_user['activities_completed'] += 1
        
        new_rank = self.define_rank()
        
        self.update_display()
        
        # Check for rank up
        if old_rank != new_rank:
            emoji = self.achievement_emojis.get(new_rank, '🎯')
            messagebox.showinfo("🎉 RANK UP!", 
                f"Congratulations!\n\n"
                f"{emoji} You've achieved: {new_rank.upper()}!\n\n"
                f"Activity '{activity['activity_name']}' completed!\n"
                f">> Earned: +{activity['activity_points']} points\n"
                f">> Total: {self.current_user['total_points']} points")
        else:
            messagebox.showinfo("✓ Success", 
                f"Activity '{activity['activity_name']}' completed!\n\n"
                f">> Earned: +{activity['activity_points']} points\n"
                f">> Total: {self.current_user['total_points']} points")
    
    def redeem_reward(self):
        """Handle reward redemption"""
        idx = self.get_selected_reward_index()
        if idx is None:
            messagebox.showwarning("⚠ No Selection", "Please select a reward to redeem!")
            return
        
        reward = self.df_rewards.iloc[idx]
        
        if self.current_user['total_points'] < int(reward['reward_price']):
            messagebox.showerror("✗ Insufficient Points", 
                f"Required: {reward['reward_price']} points\n"
                f"Available: {self.current_user['total_points']} points\n\n"
                f"Need {int(reward['reward_price']) - self.current_user['total_points']} more points!")
            return
        
        confirm = messagebox.askyesno("⚡ Confirm Redemption", 
            f"Redeem: {reward['reward_name']}\n"
            f"Cost: {reward['reward_price']} points\n\n"
            f"Confirm purchase?")
        
        if confirm:
            self.current_user['total_points'] -= int(reward['reward_price'])
            self.update_display()
            messagebox.showinfo("✓ Redeemed!", 
                f"Reward '{reward['reward_name']}' claimed!\n\n"
                f">> Spent: -{reward['reward_price']} points\n"
                f">> Remaining: {self.current_user['total_points']} points")
    
    def handle_save(self):
        """Save user progress"""
        self.save_user()
        messagebox.showinfo("✓ Saved", "Progress saved to database!\n\n>> Data synchronized successfully")
    
    def on_closing(self):
        """Handle window close event with auto-save"""
        try:
            self.save_user()
            self.root.destroy()
        except:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RewardsApp(root)
    root.mainloop()