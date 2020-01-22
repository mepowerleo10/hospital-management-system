from flask_restful import Resource
from flask import Flask, send_from_directory, render_template, session, flash, redirect, request, abort
from package.user import User, NewAdmin
from package.enums import Roles


class Register():
    @staticmethod
    def get():
        is_admin = session['role_id'] == Roles.ADMIN.val()
        if is_admin:
            return render_template('/register.html')
        else:
            return redirect('/')

    @staticmethod
    def post():
        is_admin = session['role_id'] == Roles.ADMIN.val()
        if is_admin:
            first_name = request.form['first-name']
            last_name = request.form['last-name']
            email = request.form['email']
            password = request.form['password']
            conf_password = request.form['conf-password']
            """ user = User(first_name, last_name, email, password,
                        conf_password, Roles.ADMIN.val()) """
            user = NewAdmin(first_name, last_name, email,
                            password, conf_password)

            if user.register(user):
                return redirect("/login")
            else:
                return redirect("/register")
        else:
            return redirect('/')
