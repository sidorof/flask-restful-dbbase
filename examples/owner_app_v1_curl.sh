# owner_app_v1_curl.sh


# post an order, but no authentication
curl http://localhost:5000/orders \
    -d owner_id=1

# post an order, but the wrong user
curl -H "Content-Type: application/json" \
     -H "Authorization: User:2" \
     http://localhost:5000/orders
     -d owner_id = 2

# post an order, with the right user
curl -H "Content-Type: application/json" \
     -H "Authorization: User:2" \
     -d 'owner_id = 2' \
     http://localhost:5000/orders

# get orders, no authorization
curl http://localhost:5000/orders

{
    "message": "Unauthorized User"
}

# get orders, no authorization
curl -H "Content-Type: application/json" \
     -H "Authorization: User:1" \
     http://localhost:5000/orders


# select collection of orders
curl http://localhost:5000/orders



curl -H "Content-Type: application/json" \
     -H "Authorization: User:1" \
     http://localhost:5000/orders

