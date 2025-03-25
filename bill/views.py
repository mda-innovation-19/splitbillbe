import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_bill(request):
    deserialize = json.loads(request.body)
    title = deserialize['title']
    created_by = User.objects.get(id=deserialize['created_by'])
    new_bill = Bill.objects.create(title=title, created_by=created_by)
    new_bill.save()

    amount = 0

    for item in deserialize['items']:
        item_name = item['item_name']
        quantity = item['quantity']
        price = item['price']
        amount += quantity * price

        new_item = Billitem.objects.create(item_name=item_name, quantity=quantity, price=price, bill=new_bill)
        new_item.save()

    service_fee = deserialize['service_fee']
    tax = deserialize['tax']
    discount = deserialize['discount']
    total_amount = amount + service_fee + tax - discount

    new_bill.amount = amount
    new_bill.service_fee = service_fee
    new_bill.tax = tax
    new_bill.discount = discount
    new_bill.total_amount = total_amount
    new_bill.save()

    return JsonResponse({'message': 'Bill created successfully'}, status=201)

def get_bill_by_user_id(request, user_id):
    user = User.objects.get(id=user_id)
    bills = Bill.objects.filter(created_by=user)

    result = []

    for bill in bills:

        participant = []
        paid = 0
        for bill_split in BillSplit.objects.filter(bill=bill):
            participant.append(bill_split.participant)
            if bill_split.paid:
                paid += 1

        result.append({
            'id': bill.id,
            'title': bill.title,
            'amount': bill.amount,
            'service_fee': bill.service_fee,
            'tax': bill.tax,
            'discount': bill.discount,
            'total_amount': bill.total_amount,
            'total_participant': len(participant),
            'total_paid': paid,
            'participant': participant
        })

    return JsonResponse(result, safe=False)

@csrf_exempt
def delete_bill(request, bill_id):
    bill = Bill.objects.get(id=bill_id)
    bill.delete()

    return JsonResponse({'message': 'Bill deleted successfully'}, status=200)

@csrf_exempt
def create_split_bill(request):
    deserialize = json.loads(request.body)
    bill = Bill.objects.get(id=deserialize['bill_id'])
    participant = User.objects.get(id=deserialize['participant_id'])

    total_amount = 0
    split_bill_item = []
    
    for item in deserialize['items']:
        billitem = Billitem.objects.get(id=item['billitem_id'])
        quantity = item['quantity']
        price = billitem.price
        amount = quantity * price
        total_amount += amount

        split_bill_item.append({
            'billitem_id': billitem.id,
            'quantity': quantity,
            'price': price,
            'amount': amount
        })
    
    tax = bill.tax
    service_fee = bill.service_fee
    discount = bill.discount
    total_amount += tax + service_fee - discount

    new_split = BillSplit.objects.create(bill=bill, participant=participant, tax=tax, service_fee=service_fee, discount=discount, total_amount=total_amount)
    new_split.save()

    return JsonResponse({'message': 'Bill split created successfully'}, status=201)

def get_split_bill_by_id(request, split_bill_id):
    split_bill = BillSplit.objects.get(id=split_bill_id)

    split_item = Billitem.objects.filter(bill=split_bill.bill)

    return JsonResponse({
        'id': split_bill.id,
        'bill': split_bill.bill.id,
        'participant': split_bill.participant.id,
        'tax': split_bill.tax,
        'service_fee': split_bill.service_fee,
        'discount': split_bill.discount,
        'total_amount': split_bill.total_amount,
        'items': [
            {
                'id': item.id,
                'item_name': item.item_name,
                'quantity': item.quantity,
                'price': item.price,
            }
            for item in split_item
        ]
    }, status=200)