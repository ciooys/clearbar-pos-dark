
# Clearbar POS - Dark Demo (Flask)

这是一个暗金风格的清吧收银系统演示包，基于 Flask + SQLite，包含：
- 扫码点单（H5）
- 后台收银台（暗金风）
- 会员基础、寄酒系统、优惠券、库存示例
- 可直接部署到 Render（或本地运行）

## 快速运行（本地）
1. 解压
2. 安装 Python 3.10+ 依赖：
   ```
   pip install -r requirements.txt
   ```
3. 启动：
   ```
   gunicorn app:app --bind 0.0.0.0:5000
   ```
4. 访问：
   - 后台（收银）: http://localhost:5000/admin
   - 顾客下单（H5）: http://localhost:5000/h5/order
   - 初始管理员： admin / password123

## 在 Render 部署（推荐）
1. 注册并登录 https://render.com
2. 在 Render 仪表盘点击 "New" -> "Web Service"
3. 连接你的 GitHub 仓库（或者直接上传 ZIP）
4. 填写：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. 部署成功后，Render 会给你一个可访问的 URL。

> 如果你需要，我可以把这个包给你打包下载，或指导你一步步把它部署到 Render 上。

