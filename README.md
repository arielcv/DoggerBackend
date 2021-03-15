# DoggerBackend
A backend for the Dogger Application

Aplicación destinada a conectar dueños de perros (Owners) con paseadores de perros (Walkers).
* Los perros no son un usuario directamente de la aplicación. Son el objeto de los paseos y pueden tener distintos tamaños (pequeño, mediano y grande)
* Los primeros pueden agregar perros a la aplicación, reservar paseos a paseadores específicos o a paseadores en particular. Además pueden cambiar los datos de sus perros y cancelar sus citas
* Los segundos pueden agregar agregar restricciones de paseo en caso de que solo deseen pasear a determinados perros en determinados horarios. Pueden revisar sus reservaciones pendientes y aceptarlas o rechazarlas. Además pueden aceptar reservaciones que no tengan un paseador asignado

El backend implementa una API para la aplicación Dogger. Los endpoints son:

//Acceso a los datos básicos de usuario: Nombre de Usuario y Contraseña [GET]
* url(r'^users/(?P<name>[a-zA-Z0-9_.-]+)/$', views.getUser, name='user'),

//Lista los dueños de perros [GET]
* url(r'^owners/$', views.dogOwnerList ,name = 'dogOwnerList'),

//Permite el registro de dueños de perros [POST]
* url(r'^owners/signup/$', views.dogOwnerSignUp ,name = 'dogOwnerSignUp'),

//Permite el acceso a los detalles del perfil y su modificación de cada dueño de perro a través de su Id [GET,POST]
* url(r'^owners/(?P<ownerId>[0-9]+)/$', views.dogOwnerDetails, name= 'dogOwnerDetail'),

//Permite a un dueño realizar una reservación a través de su Id
* url(r'^owners/reservation/(?P<ownerId>[0-9]+)/$', views.dogOwnerReservation, name= 'dogOwnerDetail'),

// Permite listar los perros
* url(r'^dogs/$', views.dogList ,name = 'dogOwnerList'),

//Permite listar a todos los perros de un dueño específico a través de su Id
* url(r'^dogs/owner/(?P<ownerId>[0-9]+)/$', views.dogListByOwner, name= 'dogOwnerDetail'),

//Permite acceder a los detalles de un perro y modificarlo usando su Id
* url(r'^dogs/(?P<dogId>[0-9]+)/$', views.dogDetails, name= 'dogOwnerDetail'),

//Permite realizar una modificación en una reservación: aceptarla por parte de un paseador o cancelarla por parte de cualquiera de los 2
* url(r'^reservation/(?P<reservationId>[0-9]+)/$', views.modifyReservation, name= 'dogOwnerDetail'),

//Permite obtener una lista de todos los paseadores
* url(r'^walkers/$', views.dogWalkerList ,name = 'dogOwnerList'),

//Permite registrar a un paseador
* url(r'^walkers/signup/$', views.dogWalkerSignUp ,name = 'dogOwnerList'),

//Permite realizar una reservación sin especificar un paseador
* url(r'^walkers/reservation/$', views.dogWalkerReservationToAll ,name = 'reservationToAll'),

//Permite obtener todas las reservaciones de un paseador, modificarlas y agregar
* url(r'^walkers/reservation/(?P<walkerId>[0-9]+)$', views.dogWalkerReservationList, name='dogOwnerDetail'),

//Permite obtener los detalles del perfil o modificarlos para un paseador
* url(r'^walkers/(?P<walkerId>[0-9]+)/$', views.dogWalkerDetails, name= 'dogOwnerDetail'),

//Permite obtener una lista de todas las restricciones que tiene impuestas un paseador
* url(r'^walkers/constraints/(?P<walkerId>[0-9]+)/$', views.dogWalkerConstraintsList, name='dogOwnerDetail'),

//Permite obtener los detalles de una restricción o eliminarla
* url(r'^constraints/(?P<constraintId>[0-9]+)$', views.dogWalkerConstraintsDetails, name='dogOwnerDetail'),

//Permite la autenticación mediante el uso de un token 
* url(r'^login/$', token.obtain_auth_token),
