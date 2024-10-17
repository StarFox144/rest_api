app=Flask(__name__)
api=Api(app)

items=[]

class item(Resource):
    def get(self,name):
        for items in items:
            if team['name']==name:
                return jsonify(item)
            return {'message':'item not found'},404
    
    def post(self):
        data = request.get_json()
        new_item={
            'name':data['name'],
            'price':data['price']
        }
        items.append(new_item)
        return jsonity(new_item)

    def delete(self,name):
        global items
        items=[items for item in item if item['name']!=name]
        return{'message':'Item delted'}    

api.add_resource(Item, '/item/<string:name>','/item')

if __name__=='__main__':
    app.run(debug=True)