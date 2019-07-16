import os
from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

__author__ = 'DanielPesa'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def read_excel_file(route):
    '''This function reads the spreadsheet into a pandas dataframe'''
    sheet = pd.read_excel(route)
    sheet = sheet.dropna()
    return sheet

def read_csv_file(route):
    '''This function reads the spreadsheet into a pandas dataframe'''
    sheet = pd.read_csv(route)
    sheet = sheet.dropna()
    return sheet

def plot_subplots(sheet_name,columns_list):
    '''This function plots every exercise into a different barplot in separated subplots'''
    plt.figure(figsize = (20,10))
    for i in range(len(columns_list)):
        plt.subplot(6,4,i+1)
        sns.barplot(data = sheet_name, x = 'WEEK', y = columns_list[i])
        plt.title(columns_list[i])
        plt.ylabel('Quantity')
        plt.subplots_adjust(hspace = 1, wspace = 1)
        plt.tight_layout()
    plt.show()
    #plt.savefig('static/Exercises Progress.jpg')

def plot_mean(mean_values):
    '''This function plot a barplot with the mean of every exercise'''
    plt.figure(figsize = (20,10))
    sns.barplot(data = mean_values, x = mean_values.index, y = 'mean')
    plt.xticks(rotation = 45)
    plt.ylabel('Quantity')
    plt.title('Exercises Mean')
    plt.show()
    #plt.savefig('static/Exercises Mean.jpg')

def delete_files():
    files_list = os.listdir('static/')
    for i in range(len(files_list)):
        file = files_list[i]
        os.remove('static/'+ str(file))
    print('The folder tmp has the following files: ', files_list)
    files_list_img = os.listdir('static/')
    for i in range(len(files_list_img)):
        file_img = files_list_img[i]
        os.remove('tmp'+ str(file_img))
    print('The folder static has the following files: ', files_list_img)

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        
    return render_template("complete.html")

@app.route('/complete',methods = ['POST'])
def result():
    files_list = os.listdir('static/')
    for i in range(len(files_list)):
        file = files_list[i]
        if file.endswith('.csv'):
            sheet = read_csv_file('static/'+ str(file))
        elif file.endswith('.xlsx'):
            sheet = read_excel_file('static/' + str(file))
    columns_list = sheet.columns[1:]
    describe_table = sheet.describe().round(1)
    mean_values = pd.DataFrame(describe_table.loc['mean'])
    mean_values.sort_values(by = 'mean', inplace = True, ascending = False)
    plot_subplots(sheet,columns_list)
    plot_mean(mean_values)
            
    return render_template("images.html")


if __name__ == "__main__":
    app.run(port = 4555, debug = True)

    