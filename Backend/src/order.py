from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED,HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from src.database import Order,OrderDetail,User,Product,db

order = Blueprint("order", __name__, url_prefix="/api/v1/order")


@order.post('/add')
@jwt_required()
def addOrder():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    contactNumber = request.json['contactNumber']
    shippingAddress = request.json['shippingAddress']
    total = request.json['total']
    userId = get_jwt_identity()
    orderDetails = request.json.get('orderDetails',[])

    order = Order(
        firstName = firstName,
        LastName =lastName,
        contactNumber = contactNumber,
        shippingAddress = shippingAddress,
        status = 'Processing',
        total = total,
        userId = userId

    )

    for orderDetail in orderDetails:
        quantity = orderDetail.get('quantity')
        price = orderDetail.get('price')
        subtotal = orderDetail.get('subtotal')
        productId = orderDetail.get('productId')
        if productId:
            detail = OrderDetail(quantity=quantity, price=price,subtotal=subtotal,productId=productId,order=order)
            db.session.add(detail)

    db.session.add(order)
    db.session.commit()

    return jsonify({
        'message': "Order added successfully",
        'data': {
            'id': order.id
        },"success":True

    }), HTTP_201_CREATED




@order.get('/get/all')
@jwt_required()
def getAllOrders():
    orders = Order.query.all()
    order_list = []
    for order in orders:
        user = User.query.filter_by(id=order.userId).first()
        order_data = {
            'id': order.id,
            'firstName': order.firstName,
            'LastName': order.LastName,
            'contactNumber': order.contactNumber,
            'shippingAddress': order.shippingAddress,
            'status': order.status,
            'total': order.total,
            'orderDate': order.created_at,
            'user':user.username
        }

        order_list.append(order_data)
    return jsonify({'message': "category list",'data':order_list,"success":True}), HTTP_200_OK


@order.get('/getOrderByUser')
@jwt_required()
def getOrdersForCurrentUser():
    userId = get_jwt_identity()
    orders = Order.query.filter_by(userId=userId).all()
    order_list = []
    for order in orders:
        order_data = {
            'id': order.id,
            'firstName': order.firstName,
            'LastName': order.LastName,
            'contactNumber': order.contactNumber,
            'shippingAddress': order.shippingAddress,
            'status': order.status,
            'total': order.total,
            'orderDate': order.created_at,
        }
        # detail_list=[]
        # for detail in order.orderDetails:
        #     product = Product.query.filter_by(id=order.productId).first()
        #     _data={
        #         'id':detail.id,
        #         'quantity':detail.quantity,
        #         'price':detail.price,
        #         'subtotal':detail.subtotal,
        #         'quantity':detail.quantity,
        #         'product':product.productName
        #     }
        #     tag_list.append(tag_data)
        # product_data['tags']=tag_list
        order_list.append(order_data)
    return jsonify({'message': "category list",'data':order_list,"success":True}), HTTP_200_OK


@order.get('/get/details/<int:id>')
@jwt_required()
def getOrderDetails(id):
    orderDetails = OrderDetail.query.all(orderId=id)
    detail_list=[]
    for detail in orderDetails:
        product = Product.query.filter_by(id=detail.productId).first()
        _data={
            'id':detail.id,
            'quantity':detail.quantity,
            'price':detail.price,
            'subtotal':detail.subtotal,
            'quantity':detail.quantity,
            'product':product.productName
        }
        detail_list.append(_data)
    return jsonify({'message': "details",
                    'data':detail_list,"success":True
                    }
                ), HTTP_200_OK

@order.put('/cancel')
@jwt_required()
def cancel():
    id = request.json['id']
    order = Order.query.filter_by(id=id).first()
    if order is None:
         return jsonify({'message': 'order not found',"success":False}), HTTP_404_NOT_FOUND
   
    order.status = 'Cancelled'
    db.session.commit()
    return jsonify({'data':{
        'id': order.id
    },'message':"Order cancelled successfully","success":True}), HTTP_200_OK