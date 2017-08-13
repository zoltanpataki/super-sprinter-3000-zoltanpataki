from flask import Flask, render_template, redirect, request, session, url_for
import csv

app = Flask(__name__)
form_selectkeys = ['planning', 'to-do', 'in-progress', 'review', 'done']


def makeselectblock(selectkeys, selectedoption=None):
    
    result = []
    for item in selectkeys:
        result.append(('"{}"'.format(item), item))

    if(selectedoption is None):
        return result
    else:
        for index, item in enumerate(result):
            if item[1] == selectedoption:
                result[index] = ('"{}" selected'.format(selectedoption), selectedoption)
                break
        return result


def import_story(filename="story.csv"):
    file = open(filename, 'r')
    reader = csv.reader(file)
    table = []
    for row in reader:
        table.append(row)
    print(table)
    return table


def get_last_row(csv_filename):
    with open(csv_filename, 'r') as f:
        lastrow = None
        for lastrow in csv.reader(f):
            pass
        return lastrow


def export_story(user_story, filename="story.csv"):
    with open(str(filename), 'a', newline='') as outputstream:
        writer = csv.writer(outputstream)
        writer.writerow(user_story)


def updatecsv(dictionary):
    label_list = ["title", "note", "criteria", "quantity", "time", "status"]
    filecontents = import_story()
    updatedinput = [dictionary['id']]
    line_id = int(dictionary['id'])-1

    for item in label_list:
        if(item in dictionary.keys()):
            updatedinput.append(dictionary[item])
        else:
            return False

    updatedinput[-1] = updatedinput[-1].strip('"')
    filecontents[line_id] = updatedinput

    writer = csv.writer(open('story.csv', 'w'))

    for item in filecontents:
        writer.writerow(item)
    return True


@app.route('/')
def route_index():
    database = import_story()
    return render_template('list.html', database=database)


@app.route('/story')
def route_create():
    return render_template('form.html', data=None, selectdata=makeselectblock(form_selectkeys))


@app.route('/story-save', methods=['POST'])
def route_save():
    print('POST request received!')
    label_list = ["title", "note", "criteria", "quantity", "time", "status"]
    formdata = request.form
    create_list = []
    if get_last_row("story.csv") is None:
        create_list.append("1")
    else:
        create_list.append(int(get_last_row("story.csv")[0]) + 1)
    print(create_list)
    for label in label_list:
        for key, value in formdata.items():
            if label == key:
                create_list.append(value)
    create_list[-1] = create_list[-1].strip('"')
    export_story(create_list)
    print(create_list)
    return redirect('/')


@app.route('/story/<story_id>')
def route_edit(story_id):
    data = import_story()
    edit_row = []
    for item in data:
        if item[0] == story_id:
            edit_row = item
            break

    if edit_row:
        selected = edit_row[-1]
        return render_template("form.html", data=edit_row, selectdata=makeselectblock(form_selectkeys, selected))
    else:
        return render_template('list.html', database=database)


@app.route('/edit-story', methods=['POST'])
def route_update():
    print('POST request received!')
    formdata = request.form

    if(updatecsv(formdata)):
        print('Data updated successfully!')
    else:
        print('An error occured when updating the data!')
    return redirect('/')


@app.route('/delete/<story_id>')
def route_delete(story_id):
    result = {}

    data = import_story()

    for item in data:
        if item[0] == story_id:
            data.remove(item)
            break

    writer = csv.writer(open('story.csv', 'w'))

    for item in data:
        writer.writerow(item)

    return redirect('/')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )