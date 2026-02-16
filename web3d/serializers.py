from rest_framework import serializers
from .models import ProjectModel, PieceModel, TextureModel, PresetModel

class PresetSerializer(serializers.ModelSerializer):
    """预设棋子序列化器"""
    class Meta:
        model = PresetModel
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'edited_at')

class PieceSerializer(serializers.ModelSerializer):
    """棋子序列化器"""
    # 嵌套显示预设信息
    preset_detail = PresetSerializer(source='preset', read_only=True)
    
    class Meta:
        model = PieceModel
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'edited_at')
    
    def create(self, validated_data):
        # 自动设置当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    """项目序列化器"""
    # 嵌套显示该项目下的棋子列表
    pieces = PieceSerializer(many=True, read_only=True, source='piecemodel_set')
    
    class Meta:
        model = ProjectModel
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'edited_at')
    
    def create(self, validated_data):
        # 自动设置当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TextureSerializer(serializers.ModelSerializer):
    """纹理序列化器"""
    class Meta:
        model = TextureModel
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'edited_at')
    
    def create(self, validated_data):
        # 自动设置当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)