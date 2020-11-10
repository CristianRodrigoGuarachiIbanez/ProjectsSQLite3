import sqlite3
from tabulate import tabulate

con = sqlite3.connect('hr')
cur = con.cursor()
#==#==14. Write a query to get the average salary for all departments employing more than 10 employees.
sql= """ select department_id, job_id, avg(salary), count(*) from employees group by department_id having count(*) >10 """

sql1= """ select department_id, count(job_id), avg(salary) from employees group by department_id having count(job_id) >2 """

#==1. Write a query to find the names (first_name, last_name) and salaries of the employees who have a higher salary than the employee whose last_name='Bull'. 

sqlsub= """ select first_name,  last_name, salary from employees where salary > (select salary from employees where last_name="Bull" ) """

#==2. Write a query to find the names (first_name, last_name) of all employees who works in the IT department.

sqlsub1= """ select first_name,  last_name from employees where department_id=(select department_id from departments where depart_name = "IT%") """

#==3. Write a query to find the names (first_name, last_name) of the employees who have a manager who works for a department based in the United States.
sqlsub2= """ select first_name,  last_name from employees where manager_id in (select manager_id from departments where location_id in (select location_id from locations where country_id ="US")) """

sqlsub21= """SELECT first_name, last_name FROM employees WHERE manager_id in (select employee_id FROM employees WHERE department_id 
IN (SELECT department_id FROM departments WHERE location_id 
IN (select location_id from locations where country_id='US')));"""

#==4. Write a query to find the names (first_name, last_name) of the employees who are managers.

sqlsub3 = """ select first_name,  last_name from employees where employee_id in (select manager_id from employees) """


#==5. Write a query to find the names (first_name, last_name), the salary of the employees whose salary is greater than the average salary.

sqlsub4 = """ select first_name, last_name, salary from employees where salary > (select avg(salary) from employees ) """

#==6. Write a query to find the names (first_name, last_name), the salary of the employees whose salary is equal to the minimum salary for their job grade.

sqlsub5 = """ select first_name, last_name, salary from employees em where em.salary = (select min_salary  from jobs j where em.job_id = j.job_id ) """


#==7.Write a query to find the names (first_name, last_name), the salary of the employees who earn more than the average salary and who works in any of the IT departments
sqlsub6= """ select first_name, last_name, salary from employees where department_id in (select department_id from departments where depart_name like "IT%") and salary > (select avg(salary) from employees) """

#==8. Write a query to find the names (first_name, last_name), the salary of the employees who earn more than Mr. Bell.
sqlsub7= """ select first_name, last_name, salary from employees where salary > (select salary from employees where last_name = "Bell" )  """

#==9. Write a query to find the names (first_name, last_name), the salary of the employees who earn the same salary as the minimum salary for all departments
sqlsub8= """ select * from employees where salary = (select min(salary) from employees )  """
#== 10. Write a query to find the names (first_name, last_name) of the employees who are not supervisors.
sqlsub9= """ select first_name, last_name  from employees where manager_id not in (select manager_id from departments )  """

#== 11. Write a query to display the employee ID, first name, last names, salary of all employees whose salary is above average for their departments.

sqlsub10= """ SELECT employee_id, first_name 
FROM employees AS A WHERE salary > 
( SELECT AVG(salary) FROM employees WHERE department_id = A.department_id);   """

cur.execute(sqlsub10)
data= cur.fetchall()

print(tabulate(data))
