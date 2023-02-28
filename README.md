# [ecommerce](https://ebuystore.herokuapp.com/)
A full stack ecommerce website to sign in, view & filter products, add to cart, check out, make payment and view order history. Google OAuth is used as a third party to sign in. Paypal sandbox is used for payment integration.
Images are loaded from AWS S3 bucket and the website is deployed on [heroku](https://ebuystore.herokuapp.com/).

<p align="center"></br>
<img width="639" alt="ecommerce" src="https://user-images.githubusercontent.com/26730019/221915166-6e13a90a-68be-42ec-85ba-8179ac65a9b7.png">
</p>

## To run the project

Install requirements. Be sure to be in the right directory
```
pip install -r requirements
```
Run server with manage.py
```
python3 manage.py runserver
```
**Note:** 

As the images are loaded from AWS S3 bucket, you may not be able to find the images without the environment variable (AWS credentials). 
The same goes for gmail login. Although I have left paypal credentials available as it is a dummy account

## Model

A simple model with 3 tables and the user table coming from Django's allauth (gmail login). Current order is differentiated from past orders with the status boolean.
![image4](https://user-images.githubusercontent.com/26730019/221915641-50a5dd64-1604-4f2c-bbd8-abb0d65ba14b.png)



## Tech stack
- Django
- Python
- AWS S3 bucket
- Google OAuth
- Paypal API
- HTML
- CSS 
- JavaScript

