#Inspired by :
#itstytanic, 2015. Maya Python Scripting - Fence Mesh Generator [video, online]. YouTube. Available from: https://www.youtube.com/watch?v=FRYB3UxQuPk [Accessed 28 December 2022].
import maya.cmds as cmds
def defaultButtonPush(*args):
    optionOne= cmds.intSliderGrp ('firstSlider', query=True, value=True)
    optionTwo= cmds.intSliderGrp ('secondSlider', query=True, value=True)
    optionThree= cmds.intSliderGrp ('thirdSlider', query=True, value=True)
    optionFour= cmds.radioButtonGrp('firstButton', query= True, select=1)
    
    cmds.select (all=True)
    cmds.Delete (all=True)

    #copying user inputs for height and width to variables
    width= optionTwo+1
    height= optionOne+1
    #creating chain for the fence
    #creating half of link of the chain
    cmds.polyCylinder (radius=.3, height=9)
    cmds.setAttr  ( "polyCylinder1.subdivisionsHeight", 8 )
    cmds.select  ( 'pCylinder1.vtx[20:159]', replace=True)
    cmds.move  (-0.6, 0, 0, relative=True)
    cmds.select ( 'pCylinder1.vtx[40:139]', replace=True)
    cmds.move  (-0.8, 0, 0, relative=True) 
    cmds.select ( 'pCylinder1.vtx[60:119]', replace=True)
    cmds.move (-0.9, 0, 0, relative=True)
    cmds.select ( 'pCylinder1.vtx[80:99]', replace=True) 
    cmds.move (-0.4, 0, 0, relative=True)
    cmds.select ('pCylinder1.vtx[100:159]', replace=True)
    cmds.move (0, 0, 0.3, relative=True)
    cmds.select ( 'pCylinder1.vtx[120:139]', replace=True)
    cmds.move (0, 0, 0.3, relative=True) 
    cmds.select ( 'pCylinder1.vtx[20:79]', replace=True) 
    cmds.move (0, 0, -0.4, relative=True) 
    cmds.select ( 'pCylinder1.vtx[40:59]', replace=True) 
    cmds.move (0, 0, -0.5, relative=True)
    cmds.select ('pCylinder1') 
    #now, creating the other half by duplicating and rotating
    cmds.duplicate (returnRootsOnly=True)
    cmds.rotate (0, 180, 0)
    cmds.select (all=True)
    cmds.group (name='link1')
    
    #creating links width-wise
    for count in range (2, width):
        nameNow= ('link' + str(count))
        previous= str(count-1)
        cmds.duplicate (name= nameNow)
        cmds.move (5, 0, 0, relative=True)
        
    #grouping all current links together
    cmds.select (all=True)
    cmds.group (name='linkLine1')
    cmds.select ('linkLine1')

    #creating links height-wise
    for countTwo in range (2, height):    
        nameNowAgain= ('linkLine' + str(countTwo))
        previous= str(countTwo-1)
        cmds.duplicate (name= nameNowAgain)
        cmds.move (0, 9, 0, relative=True)
    
    #making the top bar
    barLength= width*5
    barHeightFromBase= (height*9)-11
    barMoveInX= (barLength/2)-6
    cmds.polyCylinder (name='topBar', height= barLength, radius=3)
    cmds.setAttr ('polyCylinder2.subdivisionsHeight', 8)
    cmds.rotate (0, 0, 90)
    cmds.move (0, barHeightFromBase, 0, relative=True)
    cmds.move (barMoveInX, 0, 0, relative=True)

    #combining all the links to make one mesh sidemovePlaneX
    cmds.select (all=True)
    cmds.polyUnite (name='Fence')
    cmds.select (all=True)
    cmds.delete (constructionHistory=True)

    #making the plane which helps in bending the fence which can be hidden after bending
    cmds.nurbsPlane (name='Plane', lr= .5, width=10)
    cmds.setAttr ('makeNurbPlane1.patchesU', 5) 
    cmds.setAttr ('makeNurbPlane1.patchesV', 5)
    cmds.rotate (90, 0, 0, relative=True)
    cmds.rotate (0, 90, 0, relative=True)
    cmds.scale (0, width, height, relative=True)
    movePlaneInX= ((width*5)/2)-4
    movePlaneInY= ((height*9)/2)-4
    cmds.move (movePlaneInX, movePlaneInY, -2)
    
    #binding the plane to the fence
    cmds.select ('Fence')
    cmds.select ('Plane', toggle=True)
    cmds.CreateWrap ()
    
    #creating the post for the fence
    postHeight= height*9
    moveDistanceUp= (barHeightFromBase-12)/2
    cmds.polyCylinder (height= postHeight, radius=4)
    cmds.move (0, moveDistanceUp, 0, relative=True)
    cmds.move (-7.15, 0, 0, relative=True)

    #creating fence support rings
    cmds.polyTorus (radius=4.1, sectionRadius=.5, name='ring1')
    cmds.move (-7.15, 0, 0, relative=True)

    #duplicating rings and connecting with fence links at appropriate places
    for countThree in range (2, height):
        ringNames=('ring' + str(countThree))
        cmds.duplicate (name= ringNames)
        cmds.move (0, 9, 0, relative=True)

    #creating fence topper
    if optionFour == 1:
        moveDistanceTopperMain= (moveDistanceUp*2)+12
        moveDistanceTopperSecondary= (moveDistanceUp*2)+18
        cmds.polySphere (radius=6, name='fenceTopper')
        cmds.move (-7.15, 0, 0, relative=True)
        cmds.move (0, moveDistanceTopperMain, 0, relative=True)  
        cmds.polyCylinder (radius=3, height=3, name='topTopper')
        cmds.move (-7.15, 0, 0, relative=True)
        cmds.move (0, moveDistanceTopperSecondary, 0, relative=True)
        
    if optionFour == 2:
        moveDistanceTopperMain= (moveDistanceUp*2)+12
        moveDistanceTopperSecondary= (moveDistanceUp*2)+18
        cmds.polyCube (width=10, height=10, depth=10, name='fenceTopper3')
        cmds.move (-7.15, 0, 0, relative=True)
        cmds.move (0, moveDistanceTopperMain, 0, relative=True)
        cmds.polyBevel (offset= 1, segments= 1)   
        cmds.polyCylinder (radius=3, height=3, name='topTopper2')
        cmds.move (-7.15, 0, 0, relative=True)
        cmds.move (0, moveDistanceTopperSecondary, 0, relative=True)

    #creating fencing according to number of enclosed sides
    cmds.select (all=True)
    cmds.select ('Fence', toggle=True)
    cmds.delete (constructionHistory=True)

    moveFSegment= ((width-1)*5)+9
    if optionThree == 1:
        cmds.select (all=True)
        cmds.group (name='fSegment1')
        cmds.move (-7.15, 0, 0, 'fSegment1.scalePivot', 'fSegment1.rotatePivot')

    if optionThree == 2:
        cmds.select (all=True)
        cmds.group (name='fSegment1')
        cmds.move (-7.15, 0, 0, 'fSegment1.scalePivot', 'fSegment1.rotatePivot')
        cmds.duplicate (name= 'fSegment2', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.select ('fSegment2')
        cmds.rotate (0, 90, 0)
        
    if optionThree == 3:
        cmds.select (all=True)
        cmds.group (name='fSegment1')
        cmds.move (-7.15, 0, 0, 'fSegment1.scalePivot', 'fSegment1.rotatePivot')
        cmds.duplicate (name= 'fSegment2', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.duplicate (name= 'fSegment3', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.select ('fSegment2', 'fSegment3')
        cmds.group (name= 'twothree')
        adjusttwothree= ((width-2)*5)+7.15
        cmds.move (adjusttwothree, 0, 0, 'twothree.scalePivot', 'twothree.rotatePivot')
        cmds.select ('twothree')
        cmds.rotate (0, 120, 0)
        cmds.select ('fSegment3')
        cmds.rotate (0, 120, 0)
        
    if optionThree == 4:
        cmds.select (all=True)
        cmds.group (name='fSegment1')
        cmds.move (-7.15, 0, 0, 'fSegment1.scalePivot', 'fSegment1.rotatePivot')
        cmds.duplicate (name= 'fSegment2', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.duplicate (name= 'fSegment3', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.duplicate (name= 'fSegment4', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.select ('fSegment2', 'fSegment3', 'fSegment4')
        cmds.group (name= 'twothreefour')
        adjusttwothreefour= ((width-2)*5)+7.15
        cmds.move (adjusttwothreefour, 0, 0, 'twothreefour.scalePivot', 'twothreefour.rotatePivot')
        cmds.select ('fSegment3', 'fSegment4')
        cmds.group (name= 'threefour')
        adjustthreefour= (((width-2)*5)+7.15)+(((width-1)*5)+9)
        cmds.move (adjustthreefour, 0, 0, 'threefour.scalePivot', 'threefour.rotatePivot')
        cmds.select ('twothreefour')
        cmds.rotate (0, 90, 0)
        cmds.select ('threefour')
        cmds.rotate (0, 90, 0)
        cmds.select ('fSegment4')
        cmds.rotate (0, 90, 0)
        
    if optionThree == 5:
        cmds.select (all=True)
        cmds.group (name='fSegment1')
        cmds.move (-7.15, 0, 0, 'fSegment1.scalePivot', 'fSegment1.rotatePivot')
        cmds.duplicate (name= 'fSegment2', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.duplicate (name= 'fSegment3', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.duplicate (name= 'fSegment4', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.duplicate (name= 'fSegment5', returnRootsOnly=True, upstreamNodes=True, renameChildren=True)
        cmds.move (moveFSegment, 0, 0, relative=True)
        cmds.select ('fSegment2', 'fSegment3', 'fSegment4', 'fSegment5')
        cmds.group (name= 'twothreefourfive')
        adjusttwothreefourfive= ((width-2)*5)+7.15
        cmds.move (adjusttwothreefourfive, 0, 0, 'twothreefourfive.scalePivot', 'twothreefourfive.rotatePivot')
        cmds.select ('fSegment3', 'fSegment4', 'fSegment5')
        cmds.group (name= 'threefourfive')
        adjustthreefourfive= (((width-2)*5)+7.15)+(((width-1)*5)+9)
        cmds.move (adjustthreefourfive, 0, 0, 'threefourfive.scalePivot', 'threefourfive.rotatePivot')
        cmds.select ('fSegment4', 'fSegment5')
        cmds.group (name= 'fourfive')
        adjustfourfive= (((width-2)*5)+7.15)+((((width-1)*5)+9)*2)
        cmds.move (adjustfourfive, 0, 0, 'fourfive.scalePivot', 'fourfive.rotatePivot')
        cmds.select ('twothreefourfive')
        cmds.rotate(0, 72, 0)
        cmds.select ('threefourfive')
        cmds.rotate(0, 72, 0)
        cmds.select ('fourfive')
        cmds.rotate(0, 72, 0)
        cmds.select ('fSegment5')
        cmds.rotate(0, 72, 0)

mainwindow= cmds.window ('Fence Generator')
cmds.columnLayout ()
cmds.intSliderGrp ('firstSlider', label="Height of Fence Pole", field=True, fieldMinValue=1, fieldMaxValue=50, minValue=1, maxValue=50, value=10)
cmds.intSliderGrp ('secondSlider', label="Width of Fencing", field=True, fieldMinValue=1, fieldMaxValue=50, minValue=1, maxValue=50, value=10)
cmds.intSliderGrp ('thirdSlider', label="Number of Enclosed Sides", field=True, fieldMinValue=1, fieldMaxValue=5, minValue=1, maxValue=5, value=1)
cmds.columnLayout()
radioButtonOne=cmds.radioButtonGrp( 'firstButton', label='Fence Toppers', labelArray2=['1. Circular', '2. Square'], numberOfRadioButtons=2, select=1 )
cmds.button( label='      GENERATE FENCE      ', command=defaultButtonPush )
cmds.showWindow( mainwindow )
#itstytanic, 2015. Maya Python Scripting - Fence Mesh Generator [video, online]. YouTube. Available from: https://www.youtube.com/watch?v=FRYB3UxQuPk [Accessed 28 December 2022].