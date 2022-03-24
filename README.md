![Website](https://img.shields.io/website?down_color=firebrick&down_message=offline&style=for-the-badge&up_color=springgreen&up_message=online&url=https%3A%2F%2Ftracbox.herokuapp.com%2F)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/snehangsude/tracbox?color=lightblue&style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues-raw/snehangsude/tracbox?color=crimson&style=for-the-badge)
![Twitter Follow](https://img.shields.io/twitter/follow/_Perceptron_?color=teal&style=for-the-badge)
![GitHub](https://img.shields.io/github/license/snehangsude/tracbox?color=bisque&style=for-the-badge)

# [TracBox](https://tracbox.herokuapp.com/)
TracBox - A GUI built on top of Pixela API

## [Pixela](https://pixe.la/)
Pixela is the API used under the hood to make work of TracBox. Credit to [a-know](https://twitter.com/a_know) for creating and making it free to use!
You can learn more acount Pixela by clicking on the header above. 
The [Terms and Conditions](https://github.com/a-know/Pixela/wiki/Terms-of-Service) are followed based on that of Pixela.

## About the project
The aim was to make the Pixela API easier to use for users and not only us developers. Pixela helps to visualize your progress in a interactive way.
And as the saying goees - "If you can measure it, you can control it!"

#### Libraries and Languages
- HTML
- CSS
- Bootstrap
- Python
  1. Flask
  2. Flask WTForms
  3. Flask-Login
  4. Jinja
  5. SQLAlchemy
  6. Werkzeug
  7. Requests
- Heroku

#### Fonts, Icons and Images
- FontAwesome
- GoogleFonts
- Skribbl by [Manal Rakfaoui](https://www.instagram.com/lart_dimagination_/)

## FAQs
1. What information are stored by TracBox?
> Only your `username` and `password` is stored. Every other detail is directly generated using the API.

2. Pixela uses a secure token - how is that used through TracBox?
> TracBox hashes your password and uses that as the token to register, create, update and delete. Hence the requirement to logging into a session.
> *(It is recommended that you **DONOT** use `Remember Me` if you are using a public machine.)*

3. I forgot my password - what shall I do now?
> Ah! We all hate that and would love to help you get that back but unfortunately Pixela doesn't allow us to reset/retrive or change a password! 
> Plus your passwords are hashed so we don't have a way to get that back (we have but it may take decades). **Best to forget the past and start new!** 😄

4. I've mistakenly deleted my graph/account - what do I do now?
> Pretty much the above answer! Unfortunately we do not have a way to retrive it. **Note: Currently, `Delete` commands on the website doesn't pop a confirmation 
> box and would immediately remove it from the database.**

5. I'm a Patreon supporter for Pixela - why can't I use the special features?
> The website is created with the basic and the most important API calls. While it's great that you are supporting Pixela, it's yet to be integrated with
> the special features. Stay tuned for future updates!

6. I have generated a pixel but why can't I see it on the graph?
> If you have already refreshed the page and donot see it, it's cause the Pixela API puts a mark in comparison to other points. **Eg**: Say I have two dots with integer value `10` and `1`. You would initailly not be able to see a darker shade for 10 unless 1 is available as it compares value when plotting it.


## Good to know points

- Due to ease of access all forms take uppercase, camelcase and lowercase however the data is stored in lowercase
