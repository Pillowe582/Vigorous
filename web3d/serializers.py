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
    # 显示该项目下的棋子数量
    pieces_count = serializers.SerializerMethodField()  #一个自定义字段
    
    # 以后若有需要（比如团队模式），可把这个加上
    # username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = ProjectModel
        fields = [
            'id', 'name', 'description',  'feature',
            'project_tags', 'status', 'pieces_count', 
            'user', 'created_at', 'edited_at'
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'feature': {'required': False}, 
            'project_tags': {'required': False}
        }
        read_only_fields = ('created_at', 'edited_at')
    
    def create(self, validated_data):
        # 自动设置当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    # 定义计算逻辑：函数名必须是 get_<字段名>
    def get_pieces_count(self, obj):
        # obj 是当前的 ProjectModel 实例
        return obj.piecemodel_set.count()

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