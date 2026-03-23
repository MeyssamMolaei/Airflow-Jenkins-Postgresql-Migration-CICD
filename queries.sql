SELECT
  COUNT(name) as name where name is null,
  COUNT(salary) as salary where salary <= 0,
  COUNT(department) as department where department is null,
  COUNT(experience) as experience where experience <= 0,
  COUNT(education) as education where education is null,
  COUNT(city) as city where city is null,
  COUNT(tenure) as tenure where tenure <= 0,
  COUNT(skill_level) as skill_level where skill_level is null,
  COUNT(created_at) as created_at where created_at is null
  
FROM
  employees
LIMIT
  50