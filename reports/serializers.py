from rest_framework import serializers

class EventSerializer(serializers.Serializer): #Serializer for individual events
    unit = serializers.CharField() 

class EventDataSerializer(serializers.Serializer): #Main serializer for report generation input
    student_id = serializers.CharField()
    events = EventSerializer(many=True)
