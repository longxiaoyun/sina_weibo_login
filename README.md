首先四宫格手势验证码，共有24种可能，把这24种可能的图片全都保存下来，进行模型训练。
模型由好基友Bigcat实现(GitHub地址 https://github.com/zepen) 
1. process_picture.py 将图片处理成数据矩阵，保存在train_data文件夹当中；
2. train_model.py 用来训练模型，模型提供了 LR和 MLP两种模型，
   基于数据样本少于特征数，采用LR来训练模型进行分类，这部分为离线操作不参与主程序调用，
   训练好的模型存放在model文件夹当中；
3. predict_result.py 为预测部分，也是要被主程序调用部分，调用示例如下：
   ```Python
   from Image_Identification.predict_result 
   import image_identification
   image_identification(image, model_type)
   ```
   即可，
   调用上述函数会返回预测类别。
   m_dict为一个图片类别和图片命名的一个字典，将其映射起来，方便查看。 
4. login_weibo.py 执行登录脚本，需要一个微博帐号和密码。
