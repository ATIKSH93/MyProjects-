import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import random
import tkinter as tk
from tkinter import messagebox
import webbrowser

class SpotifyPlaylistCreator:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.sp_link = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                                 client_secret=client_secret,
                                                                 redirect_uri=redirect_uri,
                                                                 scope=scope))
        


    
        self.window = tk.Tk()
        self.window.title("BARALIFY")
        self.window.geometry("400x200")

        self.num_label = tk.Label(self.window, text="NUMBER OF SONGS:")
        self.num_label.grid(row=0, column=0, padx=10, pady=5)

        self.num_entry = tk.Entry(self.window)
        self.num_entry.grid(row=0, column=1, padx=10, pady=5)

        self.choice_label = tk.Label(self.window, text="WHAT DO YOU WANT TO LISTEN TO TODAY?")
        self.choice_label.grid(row=1, column=0, padx=10, pady=5)

        self.choice_entry = tk.Entry(self.window)
        self.choice_entry.grid(row=1, column=1, padx=10, pady=5)

        self.create_playlist_button = tk.Button(self.window, text="CREATE", command=self.create_playlist)
        self.create_playlist_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)




    def search_choice(self, choice):
        results = self.sp_link.search(q=choice, type='track', limit=50)
        self.tracks = results['tracks']['items']

    def select_from_choice(self, num):
        self.random_tracks = random.sample(self.tracks, num)



    def create_playlist(self):
        try:
            choice = self.choice_entry.get()
            num = int(self.num_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of songs")
            return
        
        try:
            self.search_choice(choice)
            self.select_from_choice(num)

            playlist_name = "JUST FOR YOU😊"
            playlist = self.sp_link.user_playlist_create(self.sp_link.me()['id'], playlist_name, public=False)
            playlist_id = playlist['id']
            track_uris = [track['uri'] for track in self.random_tracks]
            self.sp_link.playlist_add_items(playlist_id, track_uris)

            playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
            
            def open_link(event):
                webbrowser.open_new(playlist_url)
            
            link_label = tk.Label(self.window, text="Have a great time listening to the playlist curated\n JUST FOR YOU😊", fg="blue", cursor="hand2")
            link_label.grid(row=3, column=0, columnspan=2)
            link_label.bind("<Button-1>", open_link)
            
            messagebox.showinfo("Success", "Yeah!!!🥳🥳")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def run(self):
        self.window.mainloop()



# Initialize and run the SpotifyPlaylistCreator
client_id = '60b91fc7adc64cf9bce1597994f50b33'
client_secret = '4c80c62a3c15452298e2dd97d05028b0'
redirect_uri = 'http://127.0.0.1:8080/'
scope = 'playlist-modify-public playlist-modify-private user-library-read'
app = SpotifyPlaylistCreator(client_id, client_secret, redirect_uri, scope)
app.run()




