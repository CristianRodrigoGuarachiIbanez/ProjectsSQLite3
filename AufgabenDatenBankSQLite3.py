import os
import sqlite3
from tabulate import tabulate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "hr")
with sqlite3.connect(db_path) as conn:
    c = conn.cursor()

#sql = '''select message, amount from expenses where amount > '{}' '''.format(1)
#sql = '''select category, sum(amount) from expenses group by category having amount > '{}' '''.format(1)
#sql = '''select LastName, FirstName, ReportsTo from employees where ReportsTo >= '{}' '''.format(2)
#==1
#sql = '''select count(distinct job_id) from employees '''.format()
#==2
sql = '''select sum(distinct salary) from employees '''.format()
#==3 Write a query to get the minimum salary from employees table.
sql3 = '''select min(salary) from employees '''.format()
#==4 Write a query to get the maximum salary of an employee working as a Programmer.
sql4='''select max(salary) from employees where job_id = "IT_PROG" '''.format()

#==5  Write a query to get the average salary and number of employees working the department 90.
sql5 = '''select avg(salary), count( employee_id) from employees where department_id = 90 '''.format()

#==7. Write a query to get the number of employees with the same job.
sql7 = '''select job_id, count(employee_id) from employees group by job_id '''.format()
#==8. Write a query to get the difference between the highest and lowest salaries.
sql8 = '''select max(salary) - min(salary) difference from employees'''.format()

#==9. Write a query to find the manager ID and the salary of the lowest-paid employee for that manager.
sql9 = '''select manager_id, min(salary) from employees where manager_id is not null
          group by manager_id order by min(salary) desc'''.format()

#==11. Write a query to get the average salary for each job ID excluding programmer. <>
sql11 = '''select job_id, avg(salary) from employees where job_id is not "IT_PROG"
          group by job_id '''.format()

#==12. Write a query to get the total salary, maximum, minimum, average salary of employees (job ID wise), for department ID 90 only.
sql12 = '''select job_id, sum(salary), max(salary), min(salary), avg(salary) from employees where department_id = 90
          group by job_id '''.format()

#==13. Write a query to get the job ID and maximum salary of the employees where maximum salary is greater than or equal to $4000.
sql13 = '''select job_id, max(salary) as maximum from employees group by job_id having max(salary)>= 4000'''.format()

#==Ü1 wie viel verdienen die einzelne Mitarbeiter?
sql_ue1='''select distinct employee_id, salary from employees group by employee_id '''
#==Ü2 an welchen Ort arbeiten welche Mitarbeiter
sql_ue2=''' select department_id, employee_id  from employees '''
sql_ue22=''' select  employee_id, department_id, department_name from employees natural join department  group by employee_id'''
#==Ü3 wie heißen die Projektleiter und die von ihnen geleiteten Projekte
sql_ue3 =''' select job_title, first_name, last_name from jobs natural join employees group by job_title '''
sql_ue31 =''' select j.job_title, em.first_name, em.last_name from jobs j, employees em where j.job_id = em.job_id'''
#==Ü4 Wie viel verdienen die Mitarbeiter des Projekts, das vom Mitarbeiter mit der Personalnummer 50 geleitet wird, insgesamt
sql_ue4 = ''' select em.employee_id, j.job_id, em.salary from jobs j, employees em where j.job_id = em.job_id  
          group by em.employee_id having em.employee_id > 170 '''
#==Ü5 wie hoch sind die Deutschnittsgehälter der beteilgten Mitarbeiter je Projekt?
sql_ue5=""" select jj.job_title, avg(em.salary) from employees em, job_history j, jobs jj where em.employee_id = j.employee_id 
           and j.job_id = jj.job_id group by jj.job_title"""

sql_ue51 = """ select j.job_id, avg(salary) from employees em, job_history j where em.employee_id = j.employee_id group by j.job_id """



c.execute(sql_ue51)



tabelle = c.fetchall()

print(tabulate(tabelle))