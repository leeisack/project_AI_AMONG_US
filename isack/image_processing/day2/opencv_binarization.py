import cv2


# img_color = cv2.imread('totoro.jpg', cv2.IMREAD_COLOR)

# cv2.imshow('Color', img_color)
# cv2.waitKey(0)

# img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# cv2.imshow("Gray", img_gray)
# cv2.waitKey(0)

# cv2.destroyAllWindows()

#--------------------이진화-------------------

# img_color = cv2.imread('totoro.jpg', cv2.IMREAD_COLOR)

# cv2.imshow('Color', img_color)
# cv2.waitKey(0)

# img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# cv2.imshow("Gray", img_gray)
# cv2.waitKey(0)

# ret, img_binary = cv2.threshold(img_gray, 127, 255,cv2.THRESH_BINARY)
# # threshold(이미지화 할 대상, threshold: 이값을 기준으로 검은색 흰색 나눔,threshold크면 255로한다, threshold사용)

# cv2.imshow('Binary', img_binary)
# cv2.waitKey(0)

# cv2.destroyAllWindows()

#임계값 조절 트랙바추가
#-----------------------------------------------

# def nothing(x):
#     pass
# cv2.namedWindow('Binary')
# cv2.createTrackbar('threshold','Binary',0,255,nothing)
# cv2.setTrackbarPos('threshold','Binary',127)

# img_color = cv2.imread('totoro.jpg', cv2.IMREAD_COLOR)

# cv2.imshow('Color', img_color)
# cv2.waitKey(0)

# img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# cv2.imshow("Gray", img_gray)
# cv2.waitKey(0)

# while(True):
#     low = cv2.getTrackbarPos('threshold','Binary')
#     ret, img_binary = cv2.threshold(img_gray, low, 255,cv2.THRESH_BINARY)
#     # threshold(이미지화 할 대상, threshold: 이값을 기준으로 검은색 흰색 나눔,threshold크면 255로한다, threshold사용)

#     cv2.imshow('Binary', img_binary)
#     if cv2.waitKey(1)&0xFF == 27:
#         break

# cv2.destroyAllWindows()

#------------------------------------------------------
#임계값을 찾아내는 mask사용 

def nothing(x):
    pass
cv2.namedWindow('Binary')
cv2.createTrackbar('threshold','Binary',0,255,nothing)
cv2.setTrackbarPos('threshold','Binary',82)

img_color = cv2.imread('totoro.jpg', cv2.IMREAD_COLOR)

cv2.imshow('Color', img_color)
cv2.waitKey(0)

img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

cv2.imshow("Gray", img_gray)
cv2.waitKey(0)

while(True):
    low = cv2.getTrackbarPos('threshold','Binary')
    ret, img_binary = cv2.threshold(img_gray, low, 255,cv2.THRESH_BINARY_INV)#THRESH_BINARY가 아닌 THRESH_BINARY_INV하면 반전된 이미지얻는다 즉, 컬러가 없는부분은 없어진다.
    # threshold(이미지화 할 대상, threshold: 이값을 기준으로 검은색 흰색 나눔,threshold크면 255로한다, threshold사용)

    cv2.imshow('Binary', img_binary)

    img_result=cv2.bitwise_and(img_color, img_color, mask=img_binary)#원본이미지와 binary이미지를 and연산하는코드추가
    #binary를 mask라고 하기도한다 컬러이미지와 and연산을해서 원하는부분만 검출하는데 사용가능 
    cv2.imshow('Result',img_result)

    if cv2.waitKey(1)&0xFF == 27:
        break

cv2.destroyAllWindows()


#memo
#즉 컬러풀한 특정이미지를 보면 피사체마다 다른
#색상으로 보이지만 이를 그레이스케일하면 컬러 유사성은
#고려하지않게 한다 이를 통해 특정 임계값 이상은 255값(하얀색)
#이하는 0(검은색)으로 표현이 가능하고 이를통해 특정 객체만
#출력할 수있다. 

#만약 이를 이진화(그레이스케일) 이아닌 3원색을 다 사용
#한다면 보다더 디테일한 구분이 가능하다 