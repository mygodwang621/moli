"""
p4a build hook: 修改 AndroidManifest.xml
在 Activity 上添加 windowLayoutInDisplayCutoutMode=shortEdges
确保 Kivy Surface 以真实屏幕尺寸初始化，解决 SurfaceFlinger bufHeight 不匹配黑屏
"""
import os
import re


def hook(arch, api, libraries, dist_dir, bootstrap):
    manifest_path = os.path.join(dist_dir, 'src', 'main', 'AndroidManifest.xml')
    if not os.path.exists(manifest_path):
        print(f'[hook] AndroidManifest.xml not found at {manifest_path}')
        return

    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 在 <activity 标签上添加 cutout 模式属性（如果还没有的话）
    if 'windowLayoutInDisplayCutoutMode' not in content:
        content = content.replace(
            'android:name="org.kivy.android.PythonActivity"',
            'android:name="org.kivy.android.PythonActivity"\n'
            '        android:windowLayoutInDisplayCutoutMode="shortEdges"'
        )
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('[hook] Added windowLayoutInDisplayCutoutMode=shortEdges to AndroidManifest.xml')
    else:
        print('[hook] windowLayoutInDisplayCutoutMode already present, skipping')
