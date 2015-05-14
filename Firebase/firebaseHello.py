from firebase import firebase

firebase = firebase.FirebaseApplication('https://radiant-torch-9117.firebaseio.com/', None)
#firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
result = firebase.get('/users', '1')
print result

new_user = 'Ozgur Vatansever'

result = firebase.post('/users', new_user, {'print': 'silent'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print result