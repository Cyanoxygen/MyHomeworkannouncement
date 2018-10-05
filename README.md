# Announcement

注意，该程序可能会引起不适。

随手写的班级作业发布页生成脚本     
Based on [jekyll-theme-h2o](https://github.com/kaeyleo/jekyll-theme-H2O)

## 需要的文件
确认你的 Web 根目录下有 [jekyll-theme-h2o](https://github.com/kaeyleo/jekyll-theme-H2O) 的 `app.min.css` （ 你需要更换它的名字以防止冲突）。      
- 如果你更改了 CSS 文件名，请将 `_header` 和 `inside_header` 文件中相应的 `<style>` 标签内容更改为相应的名称。

## 已知问题
- 无法将生成的 `index.html` 拷贝到目标目录。（目前不知道是什么问题）

## 运行
文件夹必须按照 `月-日` 格式命名；你也可以更改 `go.py, addinside.py` 的 `format_date` 正则式。 
此时运行 `./go.py` 即可。

手机码字，有机会再完善。