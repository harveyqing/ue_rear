#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# from flask_script import Manager, Server
from ueBackstage.app import create_app

if __name__ == '__main__':
	create_app().run(port=5001)
	# print a.config.static_folder
	# print create_app().static_folder

# manager = Manager(create_app)
# manager.add_option('-c', '--config',  dest='config', required=False)
# manager.add_command('runserver', Server())

# @manager.command 
# def createdb():
# 	from ueBackstage.models import db
# 	db.create_all()

# if __name__ == '__main__':
# 	manager.run()