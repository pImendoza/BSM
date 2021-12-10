from app import db,question

question1 = question(question='Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.You may assume that each input would have exactly one solution, and you may not use the same element twice.You can return the answer in any order. The answer to this question will be run this test case: nums = [3,2,4], target = 6',
answer ='[1,2]',difficulty = 'easy',catergory_id = 'Algorthim')

question2 = question(question='You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.You may assume the two numbers do not contain any leading zero, except the number 0 itself. The answer to this question will be run this test case: l1 = [2,4,3], l2 = [5,6,4]',
answer ='[7,0,8]',difficulty = 'medium',catergory_id = 'Algorthim')


question3 = question(question='Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.The overall run time complexity should be O(log (m+n)).The answer to this question will be run this test case:  nums1 = [1,2], nums2 = [3,4]',
answer ='2.5',difficulty = 'hard',catergory_id = 'Algorthim')

question4 = question(question='Given an integer x, return true if x is palindrome integer. An integer is a palindrome when it reads the same backward as forward. For example, 121 is palindrome while 123 is not.The answer to this question will be run this test case:  x = -121',
answer ='false',difficulty = 'easy',catergory_id = 'Algorthim')


question5 = question(question='Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-231, 231 - 1], then return 0. The answer to this question will be run this test case:x = -123',
answer ='-321',difficulty = 'medium',catergory_id = 'Algorthim')


question6 = question(question='You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.Merge all the linked-lists into one sorted linked-list and return it. The answer to this question will be run this test case:lists = [[1,4,5],[1,3,4],[2,6]]',
answer ='[1,1,2,3,4,4,5,6]',difficulty = 'hard',catergory_id = 'Algorthim')

question7 = question(question='Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same.Since it is impossible to change the length of the array in some languages, you must instead have the result be placed in the first part of the array nums. More formally, if there are k elements after removing the duplicates, then the first k elements of nums should hold the final result. It does not matter what you leave beyond the first k elements.Return k after placing the final result in the first k slots of nums.Do not allocate extra space for another array. You must do this by modifying the input array in-place with O(1) extra memory. The answer to this question will be run this test case:nums = [0,0,1,1,1,2,2,3,3,4]',
answer ='5',difficulty = 'easy',catergory_id = 'Algorthim')


question8 = question(question='Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.It is guaranteed that the number of unique combinations that sum up to target is less than 150 combinations for the given input.  The answer to this question will be run this test case:candidates = [2,3,5], target = 8',
answer ='[[2,2,2,2],[2,3,3],[3,5]]',difficulty = 'medium',catergory_id = 'Algorthim')

question9 = question(question='Given a linked list, reverse the nodes of a linked list k at a time and return its modified list.k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.You may not alter the values in the lists nodes, only nodes themselves may be changed. The answer to this question will be run this test case:head = [1,2,3,4,5], k = 2',
answer ='[2,1,4,3,5]',difficulty = 'hard',catergory_id = 'Algorthim')

db.session.add(question1)
db.session.add(question2)
db.session.add(question3)
db.session.add(question4)
db.session.add(question5)
db.session.add(question6)
db.session.add(question7)
db.session.add(question8)
db.session.add(question9)