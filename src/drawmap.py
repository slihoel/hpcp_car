import Obstacle as obs
import math

def getMap(level=1):
    obstacles = []
    tile_size = 50

    def place_rotated_wall(x, y, w, h, angle_rad):
        # 這裡不再強制對齊 50 網格，而是根據中心點旋轉
        img = "assets/red_wall.png" # 轉角建議用統一色或特殊弧形圖
        obstacles.append(obs.Obstacle(x, y, w, h, img, angle=angle_rad))

    def place_tile(x, y):
        grid_x = x // tile_size
        grid_y = y // tile_size
        img = "assets/red_wall.png" if (grid_x + grid_y) % 2 == 0 else "assets/white_wall.png"
        obstacles.append(obs.Obstacle(x + 25, y + 25, tile_size, tile_size, img))

    if level == 1:
        # --- 基礎參數：半寬 100 (總寬 200) ---
        tw = 100 
        
        # 軌道各段中心線座標
        h1_y = 200     # 第一段水平
        v1_x = 1500    # 第一段垂直
        h2_y = 800     # 第二段水平 (向左)
        v2_x = 500     # 第二段垂直 (向上)
        h3_y = 500     # 第三段水平 (向右)

        # --- 第一轉角 (右轉下) 邊界 ---
        h1_top_out = h1_y - tw - tile_size
        h1_bot_in  = h1_y + tw
        v1_right_out = v1_x + tw
        v1_left_in   = v1_x - tw - tile_size

        # --- 第二轉角 (下轉左) 邊界 ---
        h2_bot_out = h2_y + tw
        h2_top_in  = h2_y - tw - tile_size

        # --- 第三轉角 (左轉上) 邊界 ---
        v2_left_out = v2_x - tw - tile_size
        v2_right_in = v2_x + tw
        
        # --- 第四轉角 (上轉右) 邊界 ---
        h3_top_out = h3_y - tw - tile_size
        h3_bot_in  = h3_y + tw

        # 1. 鋪設第一段：水平向右 (0 -> 1600)
        for x in range(0, v1_right_out + tile_size, tile_size):
            place_tile(x, h1_top_out)
            if x <= v1_left_in: place_tile(x, h1_bot_in)

        # 2. 鋪設第二段：垂直向下 (50 -> 900)
        for y in range(h1_top_out + tile_size, h2_bot_out + tile_size, tile_size):
            place_tile(v1_right_out, y) # 最右外牆
            if y >= h1_bot_in and y <= h2_top_in: place_tile(v1_left_in, y)

        # 3. 鋪設第三段：水平向左 (1600 -> 400)
        for x in range(v2_left_out, v1_right_out, tile_size):
            place_tile(x, h2_bot_out) # 最底外牆
            if x >= v2_right_in and x <= v1_left_in: place_tile(x, h2_top_in)

        # 4. 鋪設第四段：垂直向上 (900 -> 400)
        # 這裡 y 軸向上，所以 range 範圍是 h3_top_out 到 h2_bot_out
        for y in range(h3_top_out, h2_bot_out, tile_size):
            place_tile(v2_left_out, y) # 最左外牆
            if y <= h2_top_in and y >= h3_bot_in: place_tile(v2_right_in, y)

        # 5. 鋪設第五段：水平向右 (400 -> 1200)
        h3_end_x = 1200
        for x in range(v2_left_out + tile_size, h3_end_x + tile_size, tile_size):
            place_tile(x, h3_top_out) # 上外牆
            if x >= v2_right_in: place_tile(x, h3_bot_in) # 下內牆

        # --- 設置終點 ---
        obstacles.append(obs.Obstacle(h3_end_x, h3_y, 50, 50, "assets/green_wall.png", id=-1))

    return obstacles