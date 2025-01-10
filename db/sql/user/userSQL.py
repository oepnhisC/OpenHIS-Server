getUserSQL= '''

select '$2b$12$KIX7WkcZ8mYg0PocxC9QnO5C.pvvVwJmVYt3/o5u/9G8FQfA1.b6e' PasswordHash,
2 fname where 1<>?

'''


getUserPermissionSQL= '''

select 1 where 1<>?

'''



updatePasswordSQL= '''

select 1 where 1<>?
and 1 <> ?
'''