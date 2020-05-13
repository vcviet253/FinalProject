import datetime
import random
import string

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.timezone import localtime, is_aware, make_aware

from app.ethereum.ethereum import Ethereum
from app.models import Ballot, BallotRegister, AddressBallotRegister
from app.forms import UserRegisterForm, OptionFormSet, BallotForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


########################### FOR ADMIN ################################
# Create your views here.
# Render dashboard
from app.utilities import decrypt, encrypt, register_email_to_ballot, handle_uploaded_files


@login_required()
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('user-dashboard')
    else:
        try:
            available_ballots_list = Ballot.objects.all().order_by('-created_on')
        except Exception as e:
            print(e)
            available_ballots_list = {}

        return render(request, 'dashboard.html', {'available_ballots_list': available_ballots_list})

################################## FOR USER REGISTER ###############################
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account {username} has been created. Login now!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']

            #Need to update all hash in address_ballot_register to correspond with new password
            address_ballot_register_list = AddressBallotRegister.objects.all()
            for item in address_ballot_register_list:
                print(item)
                ballot_id = item.ballot.ballot_id
                hash_string = make_password(password=str(request.user.id) + '$' + old_password + '$' + str(ballot_id),
                                         salt='password')
                if item.hash_string == hash_string:
                    new_hash_string = make_password(password=str(request.user.id) + '$' + new_password + '$' + str(ballot_id),
                                         salt='password')
                    item.hash_string = new_hash_string
                    item.save()


            user = form.save()
            message = 'Your credentials have changed. Your new account credentials. Username: ' \
                      + request.user.username + ' . Password: ' + new_password + '. Please save these information.'
            sendEmail = EmailMessage('Credentials changed', message, to=[request.user.email])
            sendEmail.send()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user-dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


############################### DEPLOOY NEW BALLOT #################################
@login_required
def create_ballot(request):
    if not request.user.is_superuser:
        return redirect('user-dashboard')

    if request.method == 'POST':
        optionFormset = OptionFormSet(request.POST)
        ballotForm = BallotForm(request.POST, request.FILES)
        ballot_options_list = []

        if optionFormset.is_valid() and ballotForm.is_valid():

            file = request.FILES['file']
            ballot_name = ballotForm.cleaned_data['ballot_name']
            ballot_end_date = ballotForm.cleaned_data['ballot_end_date']
            max_vote = int(ballotForm.cleaned_data['max_vote'])

            ballot_options_list = [form.cleaned_data['name'] for form in optionFormset if
                                   'name' in form.cleaned_data]
            print(ballot_options_list)

            # Get the list of entered values as dictionary to re-render the page in case needed
            initial = []
            for value in ballot_options_list:
                initial.append({'name': value})

            print(int(max_vote))

            ################ EXTRA VALIDATION ################
            # Validate options list
            if len(ballot_options_list) < 2:
                messages.warning(request, 'You must add at least 2 non-blank options')
                return render(request, 'create_ballot.html',
                              {'optionFormset': OptionFormSet(initial=initial), 'ballotForm': ballotForm})
            elif max_vote > len(ballot_options_list):
                messages.warning(request, 'Maximum votes allowed cannot exceed number of options')
                print([form for form in optionFormset])
                return render(request, 'create_ballot.html',
                              {'optionFormset': OptionFormSet(initial=initial), 'ballotForm': ballotForm})

            new_ballot = Ballot(ballot_name=ballot_name, ballot_end_date=ballot_end_date)

            ballot_end_time = ((ballot_end_date) - make_aware(datetime.datetime(1970, 1, 1))).total_seconds()

            # Call ethereum function to deploy ballot contract and get remaining data (interface, address) for ballot
            ethereum = Ethereum()
            ballot_interface = ethereum.get_ballot_abi()
            ballot_address = ethereum.register_ballot(ballot_name, ballot_end_time, ballot_options_list, int(max_vote))

            new_ballot.ballot_interface = ballot_interface
            new_ballot.ballot_address = ballot_address
            new_ballot.save()

            ballot_created_id = new_ballot.pk
            register_email_to_ballot(handle_uploaded_files(file), ballot_created_id)

            messages.success(request, f"Ballot '{ballot_name}' created successfully at address '{ballot_address}'")
            return redirect('dashboard')
        else:  # Form not valid
            ballot_options_list = [form.cleaned_data['name'] for form in optionFormset if
                                   'name' in form.cleaned_data]
            print(ballot_options_list)

            # Get the list of entered values as dictionary to re-render the page in case needed
            initial = []
            for value in ballot_options_list:
                initial.append({'name': value})
            print("FORM INVALID")
            return render(request, 'create_ballot.html',
                          {'optionFormset': OptionFormSet(initial=initial), 'ballotForm': ballotForm})

    elif request.method == 'GET':
        optionFormset = OptionFormSet()
        ballotForm = BallotForm()
        return render(request, 'create_ballot.html',
                      {'optionFormset': optionFormset, 'ballotForm': ballotForm})

@login_required
def view_ballot(request, param_ballot_id):
    ballot_id = int(param_ballot_id)
    ballot = Ballot.objects.get(pk=ballot_id)
    if not request.user.is_superuser:
        return redirect('user-dashboard')
    if request.method == 'GET':
        ballot_address = Ballot.objects.get(pk=ballot_id).ballot_address
        eth_instance = Ethereum()

        # Get ballot info from eth network
        ballot_info = eth_instance.get_ballot_info(ballot_address)
        ballot_info['ballot_address'] = ballot_address
        ballot_info['ballot_end_date'] = make_aware(datetime.datetime.utcfromtimestamp(ballot_info['ballot_end_time']))
        ballot_info['invited_users_count'] = invited_users_count = BallotRegister.objects.filter(
            ballot_id=ballot_id).count()
        ballot_info['user_voted'] = BallotRegister.objects.filter(Q(ballot_id=ballot_id) & Q(voted=True)).count()

        #Get all voted addresses and their options
        voted_voter = AddressBallotRegister.objects.filter(ballot=ballot).exclude(tx_hash__exact='')
        voter_voted_options = {}
        for voter in voted_voter:
            voter_voted_options[voter.address] = []
            voted_index =eth_instance.get_user_info(ballot_address, voter_address=voter.address)['voter_voted_index']
            for index in voted_index:
                voter_voted_options[voter.address].append(ballot_info['ballot_options_name'][index])

        return render(request, 'view_ballot.html', {'ballot': ballot_info, 'voter_options': voter_voted_options})
    elif request.method == 'POST':
        return redirect('/view_ballot/' + str(param_ballot_id))

#################### RENDER USER DASHBOARD #######################
@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_associated_ballots_list = {}
            result_list = []
            try:
                # using prefect to get all ballots associated to current user
                # user_associated_ballots_list = Ballot.objects.prefetch_related('ballotregister_set').filter(ballotregister__user=request.user).order_by('-created_on')

                # Use select_related
                user_associated_ballots_list = BallotRegister.objects.select_related('ballot').filter(
                    user_id=request.user.id).order_by('-created_on')

                for item in user_associated_ballots_list:
                    tmp = {}
                    tmp['user_id'] = item.user_id
                    tmp['ballot_id'] = item.ballot.ballot_id
                    tmp['ballot_name'] = item.ballot.ballot_name
                    tmp['ballot_end_date'] = item.ballot.ballot_end_date
                    print(item.ballot.ballot_end_date)
                    tmp['created_on'] = item.ballot.created_on
                    print(is_aware(tmp['created_on']))
                    tmp['ballot_address'] = item.ballot.ballot_address
                    tmp['voted'] = item.voted
                    tmp['registered'] = item.registered
                    print(tmp['registered'])
                    result_list.append(tmp)

            except Exception as e:
                print(e)
                user_associated_ballots_list = {}


            return render(request, 'user_dashboard.html',
                          {'user_associated_ballots_list': result_list,
                           'time_now': make_aware(datetime.datetime.now())})

        elif request.method == 'POST':
            pwd = request.POST['user_password']
            ballot_id = request.POST['ballot_id']

            # Check with database registered or not
            if BallotRegister.objects.get(ballot_id=ballot_id, user_id=request.user.id).registered:
                messages.warning(request, "You already registered to this ballot")
                return redirect('user-dashboard')

            ballot = Ballot.objects.get(pk=ballot_id)
            # If password entered is correct, mark user as registered and generate ethereum address to vote
            if request.user.check_password(pwd):
                # Safety check whether an address has been created for user for this ballot
                hash_key = make_password(password=str(request.user.id) + '$' + pwd + '$' + str(ballot_id),
                                         salt='password')

                # If no address created, generate one
                if not AddressBallotRegister.objects.filter(hash_string=hash_key).exists():
                    eth_instance = Ethereum()
                    voter_address, voter_private_key = eth_instance.create_account(pwd)
                    encrypted_private_key = encrypt(voter_private_key, pwd)
                    address_ballot_register = AddressBallotRegister(hash_string=hash_key, address=voter_address,
                                                                    private_key=encrypted_private_key,
                                                                    ballot=ballot)
                    address_ballot_register.save()
                    # give_right_to_vote to address
                    print("startgive right to vote")
                    tx_hash = eth_instance.give_right_to_vote(ballot.ballot_address, voter_address,
                                                                  eth_instance.get_ballot_abi())
                    ballot_register = BallotRegister.objects.get(ballot_id=ballot_id, user_id=request.user.id)
                    ballot_register.registered = True
                    ballot_register.save()
                    messages.success(request, f'Registered succesfully. Start voting now!')
                    return redirect('/vote/' + str(ballot_id))


                # An address already existed. Try vote with this address. Maybe affected by network error
                else:
                    ballot_register = BallotRegister.objects.get(ballot_id=ballot_id, user_id=request.user.id)
                    ballot_register.registered = True
                    ballot_register.save()
                    messages.success(request, f'You are registered to vote in this ballot. Start voting now!')
                    return redirect('/vote/' + str(ballot_id))
            else:
                messages.warning(request, f'Incorrect password. Please try again')
                return redirect('user-dashboard')


##################### VOTING PROCESS ########################
@login_required
def vote(request, param_ballot_id):
    # Check if ballot_id in url is a valid ballot
    ballot_id = int(param_ballot_id)
    user_id = request.user.id
    user = request.user

    # Invalid url
    if not Ballot.objects.filter(pk=ballot_id).exists():
        return redirect('user-dashboard')

    # Check whether user is invited or not.
    if not BallotRegister.objects.filter(Q(ballot_id=ballot_id) & Q(user_id=request.user.id)).exists():
        messages.warning(request, f'You are not invited for this ballot')
        return redirect('user-dashboard')

    # If user is admin, redirect to admin dashboard
    if request.user.is_superuser:
        return redirect('dashboard')

    ballot = Ballot.objects.get(pk=ballot_id)

    if request.method == 'GET':
        # Check whether this is view or vote action to render front page
        # Can check with request.GET['action_type']. However to avoid manually entered url, should cross check with database
        user_registered = BallotRegister.objects.get(ballot_id=ballot_id, user_id=user_id).registered
        user_voted = BallotRegister.objects.get(ballot_id=ballot_id, user_id=user_id).voted

        # If ballot not ended and user not registered => They need to register
        if ballot.ballot_end_date > make_aware(datetime.datetime.now()) and user_registered == False:
            messages.warning(request, f'You need to register first')
            return redirect('user-dashboard')

        if user_voted == True:
            action_type = 'view'
            registered = True
            voted = True
            explain = "User registered and voted in time"
        elif user_voted == False:
            voted = False
            if user_registered == True and ballot.ballot_end_date > make_aware(datetime.datetime.now()):
                registered = True
                action_type = 'vote'
                explain = "Ballot's not ended, user registered but did not vote yet"
            elif user_registered == True and ballot.ballot_end_date <= make_aware(datetime.datetime.now()):
                registered = True
                action_type = 'view'
                explain = "Ballot ended, user registered but did not vote"
            elif user_registered == False and ballot.ballot_end_date <= make_aware(datetime.datetime.now()):
                registered = False
                action_type = 'view'
                explain = "Ballot ended,user did not registered in time hence did not vote"

        ballot_address = ballot.ballot_address
        eth_instance = Ethereum()

        # Get ballot info from eth network
        ballot_info = eth_instance.get_ballot_info(ballot_address)
        ballot_info['ballot_address'] = ballot_address
        ballot_info['ballot_end_date'] = make_aware(datetime.datetime.utcfromtimestamp(ballot_info['ballot_end_time']))
        ballot_info['invited_users_count'] = invited_users_count = BallotRegister.objects.filter(
            ballot_id=ballot_id).count()
        ballot_info['user_voted'] = BallotRegister.objects.filter(Q(ballot_id=ballot_id) & Q(voted=True)).count()

        print(ballot_info)
        return render(request, 'vote.html',
                      {'ballot': ballot_info, 'action_type': action_type, 'registered': registered, 'voted': voted, })

    elif request.method == 'POST' and 'vote_button' in request.POST:
        pwd = request.POST['voter_password']
        voted_index = request.POST.getlist('voted_index')
        converted_to_int_vote_index = [int(i) for i in voted_index]
        ballot_address = request.POST['ballot_address']

        # Check number of votes casted
        max_vote = request.POST['max_vote']
        max_vote = int(max_vote)

        if len(converted_to_int_vote_index) == 0 or len(converted_to_int_vote_index) > max_vote:
            messages.warning(request, f'You can only vote for {max_vote} option(s)')
            return redirect('/vote/' + str(param_ballot_id))

        tx_hash = 'none'
        if user.check_password(pwd):
            hash_key = make_password(password=str(request.user.id) + '$' + pwd + '$' + str(ballot_id), salt='password')

            # check whether a record existed in database
            address_existed = AddressBallotRegister.objects.filter(hash_string=hash_key).exists()
            if not address_existed:
                messages.warning(request, f'An error occurred. Maybe you did not register for this ballot')
                return redirect('user-dashboard')

            address_ballot_register = AddressBallotRegister.objects.get(hash_string=hash_key)
            voter_address = address_ballot_register.address
            encrypted_private_key = address_ballot_register.private_key
            private_key = decrypt(encrypted_private_key, pwd)
            eth_instance = Ethereum()

            # Cross check with solidity if this account voted in case network errors affect transaction
            user_info = eth_instance.get_user_info(ballot_address, voter_address=address_ballot_register.address)
            if user_info['voter_cast_vote']:
                ballot_register = BallotRegister.objects.get(ballot_id=ballot_id, user_id=user_id)
                ballot_register.voted = True
                ballot_register.save()
                messages.warning(request, f'An error occurred. You already voted for this ballot at some point.')
                return redirect("user-dashboard")

            # Vote with associated address then save transaction hash in database
            tx_hash = eth_instance.vote(ballot_address, converted_to_int_vote_index, voter_address,
                                        private_key, pwd)
            address_ballot_register.tx_hash = tx_hash
            address_ballot_register.save()

            # Mark voter as voted in DB
            ballot_register = BallotRegister.objects.get(ballot_id=ballot_id, user_id=user_id)
            ballot_register.voted = True
            ballot_register.save()

            messages.success(request,
                             f'Voted for ballot id {ballot_id}, address {ballot_address} successfully. Transaction hash {tx_hash}')
            return redirect("user-dashboard")
        else:
            messages.warning(request, f'Incorrect password. Please try again')
            return redirect('/vote/' + str(param_ballot_id))

    elif request.method == 'POST' and 'view_button' in request.POST:
        pwd = request.POST['voter_password_view']
        action_type = request.POST['action_type']

        if user.check_password(pwd):
            eth_instance = Ethereum()
            hash_key = make_password(password=str(request.user.id) + '$' + pwd + '$' + str(ballot_id), salt='password')
            address_ballot_register = AddressBallotRegister.objects.get(hash_string=hash_key)
            tx_hash = address_ballot_register.tx_hash
            voter_address = address_ballot_register.address

            # BALLOT INFO
            ballot_info = eth_instance.get_ballot_info(ballot.ballot_address)
            ballot_info['ballot_address'] = ballot.ballot_address
            ballot_info['ballot_end_date'] = datetime.datetime.utcfromtimestamp(ballot_info['ballot_end_time'])
            print(ballot.ballot_end_date)
            print(ballot_info['ballot_end_date'])
            print(ballot_info['ballot_end_time'])
            ballot_info['invited_users_count'] = BallotRegister.objects.filter(ballot_id=ballot_id).count()
            ballot_info['user_voted'] = BallotRegister.objects.filter(Q(ballot_id=ballot_id) & Q(voted=True)).count()
            print(ballot_info['user_voted'])

            # USER INFO
            user_info = eth_instance.get_user_info(ballot.ballot_address, voter_address)
            user_info['registered'] = BallotRegister.objects.get(user_id=user_id, ballot_id=ballot_id).registered
            user_info['voted'] = BallotRegister.objects.get(user_id=user_id, ballot_id=ballot_id).voted
            user_info['voter_address'] = voter_address
            user_info['transaction_hash'] = tx_hash

            user_info['voter_voted_name'] = []
            for index in user_info['voter_voted_index']:
                user_info['voter_voted_name'].append(ballot_info['ballot_options_name'][index])

            print(user_info)

            return render(request, 'vote.html',
                          {'ballot': ballot_info, 'action_type': action_type, 'user_info': user_info,
                           'registered': user_info['registered'], 'voted': user_info['voted']})
        else:
            messages.warning(request, f'Incorrect password. Please try again')
            return redirect('/vote/' + str(param_ballot_id))
    elif request.method == 'POST':
        print(request.POST)
        return redirect('/vote/' + str(param_ballot_id))

