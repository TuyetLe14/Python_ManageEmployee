
from ControllerLogin import *
from ViewLogin import *
from ModelLogin import *

server = 'LAPTOPSN\SQLEXPRESST'
database = 'qlnv'


model = ModelLogin()

login_view = LoginView(None)
controller = Controller(model, login_view)
login_view.controller = controller
login_view.mainloop()




