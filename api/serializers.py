from datetime import datetime

from rest_framework import serializers

from library.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

    def update(self, instance, validated_data):
        if validated_data.get("status", None) == "returned":
            instance.status = validated_data.get("status", instance.status)
            instance.return_date = datetime.now().date()

            # add fine if it applies
            instance_dt = datetime.combine(instance.borrowed_date, datetime.min.time())
            penalty_days = (datetime.now() - instance_dt).days
            fine = penalty_days * 5.99 if penalty_days else 0.00
            instance.fine = fine
            instance.save()

            return instance

        return super().update(instance, validated_data)
