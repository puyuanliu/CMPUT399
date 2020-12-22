def move(A,J,e):
    #   This function make the robot move from one position to another
    #   it takes the arm_controller class and the coordinate of the destination as the input
    inverse = np.linalg.inv(J)
    print("inverse is ", inverse)
    delta_theta = np.matmul(inverse, e)
    print("delta theta is",delta_theta)
    A.move(delta_theta[0],delta_theta[1])
    #obstacle = check_obstacle(A,5)
    #if check[0] == 0 and check[1] == 0:
    #    avoid(A,obstacle,(destination_x, destination_y),5)
    #else:
    #    pass
    return delta_theta
    
def test():
    A = ArmController()
    current_position= [A.get_x(), A.get_y()] #initial position of x and y
    destination_x= 13 # Following code initialize the Jacobian
    destination_y = 13
    A.move(14,0) #initial_movement
    delta_1_1 = (current_position[0] - A.get_x())/14
    delta_2_1 = (current_position[1] - A.get_y())/14
    current_position= [A.get_x(), A.get_y()]
    A.move(0,16) #initial_movement
    delta_1_2 = (current_position[0] - A.get_x())/14
    delta_2_2 = (current_position[1] - A.get_y())/14
    J = np.array([[delta_1_1, delta_1_2],[delta_2_1, delta_2_2]]) #initial Jacobian
    J = J + [[0.00000001, 0],[0, 0.00000001]]
    delta_y = np.array([A.get_x(), A.get_y()]) #initial delta_y
    delta_y = delta_y.transpose()
    print("J is", J)
    while round(current_position[0],2) != destination_x or round(current_position[1],2) != destination_y: #When the robot has not reach the final destination
        #end_effector_x, end_effector_y, destination_x, destination_y = vision()
        # following code is the btoyden update
        current_position = np.array([A.get_x(),A.get_y()])
        e = np.array([current_position[0]-destination_x, current_position[1] - destination_y])
        e = e.transpose()
        q = move(A,J,e)
        time.sleep(1.5)
        norm = np.linalg.norm(e)
        norm = norm * norm
        J = J + np.matmul((delta_y - np.matmul(J,q))/norm, q.transpose()) + [[0.00000001, 0],[0, 0.00000001]]
        delta_y = np.array([A.get_x() - current_position[0], A.get_y() - current_position[1]])
        print("J is", J)
        print("e is",e)
        print("current position is", current_position)
        
test()
