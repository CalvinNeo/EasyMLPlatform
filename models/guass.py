#coding:utf8
#!/usr/bin/env python
# coding=gb2312

# 以上的信息随自己的需要改动吧
def print_matrix( info, m ): # 输出矩阵
    i = 0; j = 0; l = len(m)
    print info
    for i in range( 0, len( m ) ):
        for j in range( 0, len( m[i] ) ):
            if( j == l ):
                print ' |',
            print '%6.4f' % m[i][j],
        print
    print

def swap( a, b ):
    t = a; a = b; b = t

def solve( ma, b, n ):
    global m; m = ma # 这里主要是方便最后矩阵的显示
    global s; 
    
    i = 0; j = 0; row_pos = 0; col_pos = 0; ik = 0; jk = 0
    mik = 0.0; temp = 0.0
    
    n = len( m )

    # row_pos 变量标记行循环, col_pos 变量标记列循环

    print_matrix( "一开始的矩阵", m )

    while( ( row_pos < n ) and( col_pos < n ) ):
        print "位置：row_pos = %d, col_pos = %d" % (row_pos, col_pos)
        # 选主元
        mik = - 1
        for i in range( row_pos, n ):
            if( abs( m[i][col_pos] ) > mik ):
                mik = abs( m[i][col_pos] )
                ik = i


        if( mik == 0.0 ):
            col_pos = col_pos + 1
            continue

        print_matrix( "选主元", m )

        # 交换两行
        if( ik != row_pos ):
            for j in range( col_pos, n ):
                swap( m[row_pos][j], m[ik][j] )
                swap( m[row_pos][n], m[ik][n] );     # 区域之外？

        print_matrix( "交换两行", m )

        try:
            # 消元
            m[row_pos][n] /= m[row_pos][col_pos]
        except ZeroDivisionError:
            # 除零异常 一般在无解或无穷多解的情况下出现……
            return 0;
            

        j = n - 1
        while( j >= col_pos ):
            m[row_pos][j] /= m[row_pos][col_pos]
            j = j - 1

        for i in range( 0, n ):
            if( i == row_pos ):
                continue
            m[i][n] -= m[row_pos][n] * m[i][col_pos]

            j = n - 1
            while( j >= col_pos ):
                m[i][j] -= m[row_pos][j] * m[i][col_pos]
                j = j - 1

        print_matrix( "消元", m )
        row_pos = row_pos + 1; col_pos = col_pos + 1

    for i in range( row_pos, n ):
        if( abs( m[i][n] ) == 0.0 ):
            return 0
    return 1

if __name__ == '__main__':
    matrix = [[2.0,   0.0, - 2.0,   0.0], 
              [0.0,   2.0, - 1.0,   0.0], 
              [0.0,   1.0,   0.0,  10.0]]

    i = 0; j = 0; n = 0
    # 输出方程组
    print_matrix( "一开始的矩阵", matrix )

    # 求解方程组, 并输出方程组的可解信息
    ret = solve( matrix, 0, 0 )
    
    if( ret!= 0 ):
        print "方程组有解\n"
    else:
        print "方 程组无唯一解或无解\n"

    # 输出方程组及其解
    print_matrix( "方程组及其解", matrix )
    for i in range( 0, len( m ) ):
        print "x[%d] = %6.4f" % (i, m[i][len( m )])

