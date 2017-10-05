drop table if exists employee;
create table employee (
  id integer primary key autoincrement,
  fname text not null,
  lname text not null,
  phoneno text not null,
  emailid text not null,
  sal real not null,
  bdate text not null,
  jdate text not null

);
