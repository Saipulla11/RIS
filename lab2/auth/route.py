import os
from flask import render_template, request, redirect, url_for, Blueprint
from database.sql_provider import SQLProvider
from auth