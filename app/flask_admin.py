# class CustomModelView(ModelView):
#
#     def is_accessible(self):
#         if not session.get('user_id'):
#             return False
#
#         user_id = session.get('user_id')
#         user = db.session.get(User, user_id)
#         roles = [role.title for role in user.roles]
#         if RoleEnum.ADMIN.value in roles:
#             return True
#         return False
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('login', next=request.url))
#
#
# admin.add_view(CustomModelView(User, db.session))
# admin.add_view(CustomModelView(Post, db.session))
# admin.add_view(CustomModelView(IdCard, db.session))
# admin.add_view(CustomModelView(Role, db.session))