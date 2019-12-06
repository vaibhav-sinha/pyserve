# HTTP Servers, WSGI and your Web App

In our day to day work, we develop applications in our choice of framework(mostly Django) assuming that our View function would get invoked a Request object and we write code to handle that request and provide a Response.

Today, we want to explore what happens (and how) before the view function is invoked.

In the process, we will write our own HTTP Server, make it WSGI compliant and write our own mini web framework.


## HTTP Server

The aim of this part of the talk is to get us to think about and maybe answer few of the following questions

1. How do we run our app in Development?
2. How do we run it in production?
3. Why is there a difference?
4. What configuration do we use in production?
5. Why did we make that choice?
6. What options do we have?
7. Do we write our code mindful of the server configuration?
8. Can we do better?


## WSGI

1. How much effort would be to change our production web server?
2. If a lot, why? If not, why?
3. How does a web server load our app?
4. How does it interact with our app?
5. What is WSGI?
6. What is it's technical specification?
7. Are we really using it?
