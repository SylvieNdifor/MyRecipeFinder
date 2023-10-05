import requests
import os
from dotenv import load_dotenv
import tkinter as tk
from PIL import ImageTk,Image
from tkinter import messagebox
import io

load_dotenv()

def get_recipes(ingredients):
    api_key = os.getenv('SPOONACULAR_API_KEY')
    url= f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}'

    params = {'ingredients':ingredients,'number':6}

    response= requests.get(url,params=params)
    data= response.json()

    recipe_text.delete(1.0,tk.END)
    recipe_images=[]

    for i, recipe in enumerate(data, start=1):
        recipe_title=(f"{i}.{recipe['title']}(id:{recipe['id']})")
        recipe_text.insert(tk.END,recipe_title + "\n")

        try:
              # Load and resize the image
            image_url = recipe['image']
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((250, 95))
             # Resize the image to desired dimensions
            recipe_image = ImageTk.PhotoImage(image)

            recipe_text.image_create(tk.END,image=recipe_image)
            recipe_text.insert(tk.END,"\n")
            recipe_images.append(recipe_image)

            recipe_text.image= recipe_image


        except Exception as e:
            messagebox.showwarning('Error',f"Failed to load image for recipe{i}:{str(e)}")
        recipe_text.images=recipe_images
def search_button_clicked():
    ingredients= enter_ingredient.get()
    get_recipes(ingredients)


window = tk.Tk()
window.geometry('700x800')
window.configure(bg='pink')
window.title('RECIPE FINDER')

logo=tk.PhotoImage(file='img_1.png')
image_logo = tk.Label(window,image=logo, bg='pink')
image_logo.pack(anchor='e')

label = tk.Label(window,text='Enter ingredients separated by comma',fg='black',bg='pink',font=('',20,'bold'))
label.pack(pady=5)

enter_ingredient=tk.Entry(window,width=99,bg='pink',bd=5)
enter_ingredient.pack()
enter_ingredient.focus_set()

search_button=tk.Button(window,width=15,text='Search',command=search_button_clicked,font=('',20,'bold'))
search_button.pack()

recipe_text= tk.Text(window,width=100,height=50,bg='pink')
recipe_text.pack(pady=1)

window.mainloop()
