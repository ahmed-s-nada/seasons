from rest_framework import serializers
from . models import Payment, Instalment, member
# from profile.models import memberProfile
from django.utils.timezone import now


class MemberSerializer(serializers.ModelSerializer):

    # member = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = member
        fields = ['id','facebook', 'twitter', 'instagarm', 'addetional_email','password']
        extra_kwargs = {'password':{'write_only':True}}
        # read_only_fields =('member',)




class PaymentSerializer(serializers.ModelSerializer):

    instalments = serializers.HyperlinkedRelatedField( # <== The field name must be the same related name
        many=True,
        read_only=True,
        view_name='members:instalment-detail', # <= YOU MUST WRITE THE APP THEN THE VIEW
    )

    toto = serializers.SerializerMethodField()
    class Meta:

        model = Payment
        fields = ('payment_details', 'last_payment_date', 'required_fees',
                  'payments_total', 'current_credit', 'instalments', 'toto')
        # read_only_fields = ['all_instalments','payments_total',]

    def get_toto(self, obj):
        return now()


class InstallmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instalment
        fields = ( 'payment_file', 'payment_methode', 'instalment_details',
                  'instalment_date', 'instalment_value')
