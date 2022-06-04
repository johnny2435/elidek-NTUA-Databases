from flask import Blueprint, redirect, render_template, request, url_for
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="elidek"
)
mycursor = db.cursor()
variable = [['hi']]
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'available_programmes':
            return redirect(url_for('views.available_programmes'))
        elif action == 'projects':
            return redirect(url_for('views.projects'))
        elif action == 'two_views':
            return redirect(url_for('views.two_views'))
        elif action == 's_interest':
            return redirect(url_for('views.science_field_search'))
        elif action == 'o_same':
            return redirect(url_for('views.query3_4'))
        elif action == 's_pairs':
            return redirect(url_for('views.query3_5'))
        elif action == 'young_researchers':
            return redirect(url_for('views.young_researchers'))
        elif action == 'top_exec':
            return redirect(url_for('views.top_executives'))
        elif action == 'no_deliverables':
            return redirect(url_for('views.no_deliverables'))
        elif action == 'CRUD':
            return redirect(url_for('views.tables_CRUD')) 
        
    return render_template("home.html")

@views.route('/available_programmes')
def available_programmes():
    mycursor.execute("SELECT name, department from programme")
    prog_attr = []
    for x in mycursor:
        prog_attr.append(x)
    return render_template("programme.html", prog_attr = prog_attr)

@views.route('/projects', methods=['GET', 'POST'])
def projects():
    mycursor.execute("SELECT * from executive")
    exec_name = []
    for x in mycursor:
        exec_name.append(x)

    if request.method == 'POST':
        init_date = request.form.get('init_date')
        final_date = request.form.get('final_date')
        min_dur = request.form.get('min_dur')
        max_dur = request.form.get('max_dur')
        executive = request.form.get('executive')
        count = 0
        s1, s2, s3, s4, s5, s6 = '','','','','',''
        if(init_date!=''):
            count=count+1
            s2 = ' start_date >= \'' + init_date + '\' '
        if(final_date!=''):
            count=count+1
            if(count<=1):
                s3 = ' start_date <= \'' + final_date + '\' '
            else:
                s3 = ' and start_date <= \'' + final_date + '\' '
        if(min_dur!=''):
            count=count+1
            if(count<=1):
                s4 = ' duration >= ' + min_dur
            else:
                s4 = ' and duration >= ' + min_dur
        if(max_dur!=''):
            count=count+1
            if(count<=1):
                s5 = ' duration <= ' + max_dur
            else:
                s5 = ' and duration <= ' + max_dur
        if(count>0):
            s1 = ' where '

        if(executive!=''):
            mycursor.execute("SELECT p.title, p.funding_amount, p.start_date from (SELECT * from project" +s1+s2+s3+s4+s5+ ") p natural join executive e where e.full_name = '"+ executive +"'")
        else:
            mycursor.execute("SELECT title, funding_amount, start_date from project "+s1+s2+s3+s4+s5)
        return redirect(url_for('views.project_list'))
    return render_template("projects.html", exec_name = exec_name)
#SELECT p.title from (SELECT * from project where duration >= 400) p natural join executive e where e.full_name = 'Adam Black'
#SELECT p.title from project p join executive e where p.executive_id = e.executive_id and e.full_name = 'Adam Black';
@views.route('/project_list', methods=['GET', 'POST'])
def project_list():
    project_l = []
    for x in mycursor:
        project_l.append(x)
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        mycursor.execute("SELECT r.first_name, r.last_name from project p natural join works_on w natural join researcher r where p.title = '"+ project_name +"'")
        return redirect(url_for('views.researcher_list'))
    return render_template("project_list.html", project_list = project_l)

@views.route('/researcher_list')
def researcher_list():
    researcher_l = []
    for x in mycursor:
        researcher_l.append(x)
    return render_template("researcher_list.html", researcher_list = researcher_l)

@views.route('/two_views')
def two_views():
    mycursor.execute("SELECT * FROM project_researcher_view")
    first_view = []
    for x in mycursor:
        first_view.append(x)
    mycursor.execute("SELECT * FROM org_university_view")
    second_view = []
    for x in mycursor:
        second_view.append(x)
    return render_template("two_views_list.html", first_view = first_view, second_view = second_view)


#"SELECT p.title, r.first_name, r.last_name from project p join researcher r on p.project_") (((view)))

@views.route('/science_field_search', methods=['GET', 'POST'])
def science_field_search():
    mycursor.execute("SELECT name from science_field")
    science_field_list = []
    for x in mycursor:
        science_field_list.append(x)
    if request.method == 'POST':
        s_field = request.form.get('science_field')
        mycursor.execute("SELECT p.title from science_field s INNER JOIN project_science_field ps on s.science_field_id = ps.science_field_id INNER JOIN project p on p.project_id = ps.project_id WHERE p.end_date is NULL and s.name = '" + s_field +"'")
        global variable
        variable = []
        for x in mycursor:
            variable.append(x)      
        mycursor.execute("(SELECT r.first_name, r.last_name from science_field s NATURAL JOIN project_science_field ps NATURAL JOIN project p INNER JOIN researcher r ON p.supervisor_researcher_id = r.researcher_id WHERE p.end_date is NULL and s.name = '" + s_field +"') UNION ( SELECT r.first_name, r.last_name from science_field s NATURAL JOIN project_science_field ps NATURAL JOIN project p NATURAL JOIN works_on w NATURAL JOIN researcher r WHERE p.end_date is NULL and s.name = '" + s_field +"')")
        return redirect(url_for('views.science_field_res'))
    return render_template("science_field_search.html", science_field_list = science_field_list)

@views.route('/science_field_res')
def science_field_res():
    s_researcher = []
    for x in mycursor:
        s_researcher.append(x) 
    return render_template("science_field_res.html", s_project = variable, s_researcher = s_researcher)

@views.route('/query3_4')
def query3_4():
    mycursor.execute("select distinct t1.name from (select o.organisation_id, o.name, YEAR(p.start_date) AS year, count(*) as o_count from organisation o natural join project p group by year, o.organisation_id) t1 JOIN (select o.organisation_id, o.name, YEAR(p.start_date) AS year, count(*) as o_count from organisation o natural join project p group by year, o.organisation_id) t2 where t1.year = t2.year - 1 and t1.o_count = t2.o_count and t1.o_count > 9")
    org = []
    for x in mycursor:
        org.append(x) 
    return render_template("query3_4.html", org = org)

@views.route('/query3_5')
def query3_5():
    mycursor.execute("select ps1.name, ps2.name, count(*) as t_count from (select * from project p natural join project_science_field ps natural join science_field s) ps1 join (select * from project p natural join project_science_field ps natural join science_field s) ps2 where ps1.science_field_id < ps2.science_field_id and ps1.project_id = ps2.project_id group by ps1.science_field_id, ps2.science_field_id ORDER BY t_count DESC limit 3")
    couple = []
    for x in mycursor:
        couple.append(x) 
    return render_template("query3_5.html", couple = couple)

@views.route('/young_researchers')
def young_researchers():
    mycursor.execute("select pr.first_name, pr.last_name, pr.project_count from ( select r.first_name, r.last_name, count(*) as project_count from researcher r natural join works_on w join project p on w.project_id = p.project_id where DATEDIFF(CURDATE(), r.birth_date) < 14600 and p.end_date is null group by r.researcher_id ) pr join (select count(*) as project_count from researcher r natural join works_on w join project p on w.project_id = p.project_id where DATEDIFF(CURDATE(), r.birth_date) < 14600 and p.end_date is null group by r.researcher_id ORDER BY project_count desc limit 1 ) c where c.project_count = pr.project_count")
    young_researchers = []
    for x in mycursor:
        young_researchers.append(x) 
    return render_template("young_researchers.html", young_researchers = young_researchers)

@views.route('/top_executives')
def top_executives():
    mycursor.execute("select e.full_name, o.name, sum(p.funding_amount) as total from executive e natural join project p natural join organisation o natural join company c group by e.executive_id order by total desc limit 5")
    top_executives = []
    for x in mycursor:
        top_executives.append(x) 
    return render_template("top_executives.html", top_executives = top_executives)

@views.route('/no_deliverables')
def no_deliverables():
    mycursor.execute("select r.first_name, r.last_name, count(*) as project_count from researcher r natural join works_on w join  (select p.project_id from project p left join deliverable d on p.project_id = d.project_id where d.project_id is null) p1 on p1.project_id = w.project_id group by r.researcher_id having project_count > 4")
    no_deliverables = []
    for x in mycursor:
        no_deliverables.append(x) 
    return render_template("no_deliverables.html", no_deliverables = no_deliverables)

@views.route('/tables_CRUD', methods=['GET', 'POST'])
def tables_CRUD():
    if request.method == 'POST':
        table = request.form.get('table')
        if table == 'project':
            return redirect(url_for('views.proj_CRUD'))
        if table == 'organisation':
            return redirect(url_for('views.org_CRUD'))
        if table == 'researcher':
            return redirect(url_for('views.res_CRUD'))
        elif table == 'works_on':
            return redirect(url_for('views.works_on_CRUD'))
        elif table == 'executive':
            return redirect(url_for('views.exec_CRUD'))
        elif table == 'science_field':
            return redirect(url_for('views.science_field_CRUD'))
        elif table == 'project_science_field':
            return redirect(url_for('views.project_science_field_CRUD'))
        elif table == 'programme':
            return redirect(url_for('views.prog_CRUD'))
        elif table == 'company':
            return redirect(url_for('views.comp_CRUD'))
        elif table == 'university':
            return redirect(url_for('views.uni_CRUD'))
        elif table == 'research_centre':
            return redirect(url_for('views.cen_CRUD'))
        elif table == 'deliverable':
            return redirect(url_for('views.deli_CRUD'))
        elif table == 'phone_number':
            return redirect(url_for('views.phone_CRUD'))
        elif table == 'evaluates':
            return redirect(url_for('views.eval_CRUD'))
    return render_template("tables_CRUD.html")

@views.route('/org_CRUD', methods=['GET', 'POST'])
def org_CRUD():
    mycursor.execute("SELECT * from organisation")
    org_CRUD =[]
    for x in mycursor:
        org_CRUD.append(x) 
    if request.method == 'POST':
        name = request.form.get('name')
        abbr = request.form.get('abbr')
        postal_address = request.form.get('postal_address')
        street = request.form.get('street')
        city = request.form.get('city')
        action = request.form.get('action')
        id = request.form.get('ID')
        if action == 'Insert':
            mycursor.execute("Insert into organisation (name, abbreviation, postal_address, street, city) Values ('"+ name + "', '" + abbr + "', '" + postal_address+ "', '" + street + "', '" + city +"')")
            db.commit()
        if action == 'Delete':
            mycursor.execute("Delete from organisation where organisation_id = " + id)
            db.commit()
        if action == 'Update':
            mycursor.execute("Update organisation SET name = '"+ name + "', abbreviation = '" + abbr + "', postal_address = '" + postal_address+ "', street = '" + street + "', city = '" + city +"' where organisation_id = " + id)
            db.commit()
        return redirect(url_for('views.org_CRUD'))
    return render_template("org_CRUD.html", org_CRUD = org_CRUD)

@views.route('/res_CRUD', methods=['GET', 'POST'])
def res_CRUD():
    mycursor.execute("SELECT * from researcher")
    res_CRUD =[]
    for x in mycursor:
        res_CRUD.append(x) 
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birth_date = request.form.get('birth_date')
        sex = request.form.get('sex')
        employee_organisation_id = request.form.get('eo_ID')
        employee_date = request.form.get('employee_date')
        action = request.form.get('action')
        id = request.form.get('ID')
        if action == 'Insert':
            mycursor.execute("Insert into researcher (first_name, last_name, birth_date, sex, employee_organisation_id, employee_date) Values ('" + first_name + "', '" + last_name + "', '" + birth_date + "', '" + sex + "', " + employee_organisation_id + ", '" + employee_date +"')")
            db.commit()
        if action == 'Delete':
            mycursor.execute("Delete from researcher where researcher_id = " + id)
            db.commit()
        if action == 'Update':
            mycursor.execute("Update researcher SET first_name = '"+ first_name + "', last_name = '" + last_name + "', birth_date = '" + str(birth_date) + "', sex = '" + sex + "', employee_organisation_id = '" + employee_organisation_id +"', employee_date = '"+ str(employee_date) +"' where researcher_id = " + id)
            db.commit()
        return redirect(url_for('views.res_CRUD'))
    return render_template("res_CRUD.html", res_CRUD = res_CRUD)

@views.route('/proj_CRUD', methods=['GET', 'POST'])
def proj_CRUD():
    mycursor.execute("SELECT project_id, title, summary, funding_amount, start_date, end_date, executive_id, programme_id, supervisor_researcher_id, organisation_id from project")
    proj_CRUD =[]
    for x in mycursor:
        proj_CRUD.append(x) 
    if request.method == 'POST':
        title = request.form.get('title')
        summary = request.form.get('summary')
        funding_amount = request.form.get('funding_amount')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        executive_id = request.form.get('executive_id')
        programme_id = request.form.get('programme_id')
        supervisor_researcher_id = request.form.get('supervisor_researcher_id')
        organisation_id = request.form.get('organisation_id')
        action = request.form.get('action')
        id = request.form.get('ID')
        if action == 'Insert':
            mycursor.execute("Insert into project (title, summary, funding_amount, start_date, end_date, executive_id, programme_id, supervisor_researcher_id, organisation_id) Values ('" + title + "', '" + summary + "', '" + funding_amount + "', '" + start_date + "', '" + end_date + "' ," + executive_id + ", " + programme_id +  ", " + supervisor_researcher_id + ", " + organisation_id +")")
            db.commit()
        if action == 'Delete':
            mycursor.execute("Delete from project where project_id = " + id)
            db.commit()
        if action == 'Update':
            mycursor.execute("Update project SET title = '"+ title + "', summary = '" + summary + "', funding_amount = '" + funding_amount + "', start_date = '" + start_date + "', end_date = '" + end_date +"', executive_id = '"+ executive_id +"', programme_id = '"+ programme_id +"', supervisor_researcher_id = '"+ supervisor_researcher_id +"', organisation_id = '"+ organisation_id +"' where project_id = " + id)
            db.commit()
        return redirect(url_for('views.proj_CRUD'))
    return render_template("proj_CRUD.html", proj_CRUD = proj_CRUD)

@views.route('/works_on_CRUD', methods=['GET', 'POST'])
def works_on_CRUD():
    mycursor.execute("SELECT * from works_on")
    works_on =[]
    for x in mycursor:
        works_on.append(x) 
    if request.method == 'POST':
        project_id = request.form.get('project_id')
        researcher_id = request.form.get('researcher_id')
        action = request.form.get('action1')
        if action == 'Insert':
            mycursor.execute("Insert into works_on (project_id, researcher_id) Values (" + project_id + ", " + researcher_id +")")
            db.commit()
        if action == 'Delete':
            mycursor.execute("Delete from works_on where project_id = " + project_id + " and researcher_id = " + researcher_id )
            db.commit()
        return redirect(url_for('views.works_on_CRUD'))
    return render_template("works_on_CRUD.html", works_on = works_on)

@views.route('/exec_CRUD', methods=['GET', 'POST'])
def exec_CRUD():
    mycursor.execute("SELECT * from executive")
    exec_CRUD =[]
    for x in mycursor:
        exec_CRUD.append(x) 
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        action = request.form.get('action')
        id = request.form.get('ID')
        if action == 'Insert':
            mycursor.execute("Insert into executive (full_name) Values ('" + full_name + "')")
            db.commit()
        if action == 'Delete':
            mycursor.execute("Delete from executive where executive_id = " + id)
            db.commit()
        if action == 'Update':
            mycursor.execute("Update executive SET full_name = '"+ full_name +"' where executive_id = " + id)
            db.commit()
        return redirect(url_for('views.exec_CRUD'))
    return render_template("exec_CRUD.html", exec_CRUD = exec_CRUD)

@views.route('/science_field_CRUD', methods=['GET', 'POST'])
def science_field_CRUD():
    mycursor.execute("SELECT * from science_field")
    science_field_CRUD =[]
    for x in mycursor:
        science_field_CRUD.append(x) 
    if request.method == 'POST':
        name = request.form.get('name')
        action = request.form.get('action')
        id = request.form.get('ID')
        if action == 'Insert':
            mycursor.execute("Insert into science_field (name) Values ('" + name + "')")
            db.commit()
        if action == 'Delete':
            mycursor.execute("Delete from science_field where science_field_id = " + id)
            db.commit()
        if action == 'Update':
            mycursor.execute("Update science_field SET name = '"+ name +"' where science_field_id = " + id)
            db.commit()
        return redirect(url_for('views.science_field_CRUD'))
    return render_template("science_field_CRUD.html", science_field_CRUD = science_field_CRUD)

@views.route('/project_science_field_CRUD', methods=['GET', 'POST'])
def project_science_field_CRUD():
    mycursor.execute("SELECT * from project_science_field")
    project_science_field =[]
    for x in mycursor:
        project_science_field.append(x) 
    if request.method == 'POST':
        project_id = request.form.get('project_id')
        science_field_id = request.form.get('science_field_id')
        action = request.form.get('action1')
        if action == 'Insert':
            mycursor.execute("Insert into project_science_field (project_id, science_field_id) Values (" + project_id + ", " + science_field_id +")")
            db.commit()
        if action == 'Delete':
            mycursor.execute("Delete from project_science_field where project_id = " + project_id + " and science_field_id = " + science_field_id )
            db.commit()
        return redirect(url_for('views.project_science_field_CRUD'))
    return render_template("project_science_field_CRUD.html", project_science_field = project_science_field)

@views.route('/prog_CRUD')
def prog_CRUD():
    mycursor.execute("select * from programme")
    prog = []
    for x in mycursor:
        prog.append(x) 
    return render_template("prog_CRUD.html", prog = prog)

@views.route('/comp_CRUD')
def comp_CRUD():
    mycursor.execute("select * from company")
    comp = []
    for x in mycursor:
        comp.append(x) 
    return render_template("comp_CRUD.html", comp = comp)

@views.route('/uni_CRUD')
def uni_CRUD():
    mycursor.execute("select * from university")
    uni = []
    for x in mycursor:
        uni.append(x) 
    return render_template("uni_CRUD.html", uni = uni)

@views.route('/cen_CRUD')
def cen_CRUD():
    mycursor.execute("select * from research_centre")
    cen = []
    for x in mycursor:
        cen.append(x) 
    return render_template("cen_CRUD.html", cen = cen)

@views.route('/deli_CRUD')
def deli_CRUD():
    mycursor.execute("select * from deliverable")
    deli = []
    for x in mycursor:
        deli.append(x) 
    return render_template("deli_CRUD.html", deli = deli)

@views.route('/phone_CRUD')
def phone_CRUD():
    mycursor.execute("select * from phone_number")
    phone = []
    for x in mycursor:
        phone.append(x) 
    return render_template("phone_CRUD.html", phone = phone)

@views.route('/eval_CRUD')
def eval_CRUD():
    mycursor.execute("select * from evaluates")
    eval = []
    for x in mycursor:
        eval.append(x) 
    return render_template("eval_CRUD.html", eval = eval)