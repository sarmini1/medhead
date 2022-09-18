# from shotstuff.database import db

# #TODO: consider renaming this table to just regimens or something that
# # doesn't indicate that it's entirely for injectables
# # class InjectionRegimen(db.Model):
# #     """Injection Regimen."""

# #     __tablename__ = "injection_regimens"

# #     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# #     title = db.Column(db.Text, nullable=False)
# #     medication_id = db.Column(
# #         db.Integer,
# #         db.ForeignKey("medications.id", ondelete="cascade"),
# #         nullable=False
# #     )

# #     def to_dict(self):
# #         """Serialize to a dict of regimen info."""

# #         return {
# #             "id": self.id,
# #             "title": self.title,
# #             "medication_id": self.medication_id,
# #         }
