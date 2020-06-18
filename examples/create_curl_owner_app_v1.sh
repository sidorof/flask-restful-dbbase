# create_curl_owner_app_v1.sh
echo "# owner_app_v1_curl.sh" > owner_app_v1.txt


echo "# post an order, but no authentication" >> owner_app_v1.txt
echo "curl http://localhost:5000/orders \ " >> owner_app_v1.txt
echo "    -d owner_id=1" >> owner_app_v1.txt

# echo "# post an order, but the user" >> owner_app_v1.txt
# echo "curl -H "Content-Type: application/json" \ " >> owner_app_v1.txt
# echo "     -H "Authorization: User:2" \ " >> owner_app_v1.txt
# echo "     http://localhost:5000/orders" >> owner_app_v1.txt
# echo "     -d owner_id = 2" >> owner_app_v1.txt
# echo "
# echo "# post an order, with the right user" >> owner_app_v1.txt
# echo "curl -H "Content-Type: application/json" \ " >> owner_app_v1.txt
# echo "     -H "Authorization: User:2" \ " >> owner_app_v1.txt
# echo "     -d owner_id = 2 \
# echo "     http://localhost:5000/orders" >> owner_app_v1.txt
# echo "
# echo "# get orders, no authorization" >> owner_app_v1.txt
# echo "curl http://localhost:5000/orders" >> owner_app_v1.txt
#
# echo "# get orders, no authorization" >> owner_app_v1.txt
# echo "curl -H "Content-Type: application/json" \ " >> owner_app_v1.txt
# echo "     -H "Authorization: User:1" \ " >> owner_app_v1.txt
# echo "     http://localhost:5000/orders" >> owner_app_v1.txt
# echo "
# echo "
# echo "# select collection of orders" >> owner_app_v1.txt
# echo "curl -g http://localhost:5000/orders" >> owner_app_v1.txt
# echo "
# echo "
# echo "
# echo "curl -H "Content-Type: application/json" \ " >> owner_app_v1.txt
# echo "     -H "Authorization: User:1" \ " >> owner_app_v1.txt
# echo "     http://localhost:5000/orders" >> owner_app_v1.txt

