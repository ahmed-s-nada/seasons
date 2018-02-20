from rest_framework import serializers
from .models import memberProfile

class MemberSerializer(serializers.ModelSerializer):

    # member = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = memberProfile
        fields = '__all__'
        extra_kwargs = {'password':{'write_only':True}}
        read_only_fields =('member',)
