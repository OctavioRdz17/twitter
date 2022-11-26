#Python
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List
import json
# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Path
from fastapi import HTTPException

app = FastAPI()

# Models
class UserBase(BaseModel):
    user_id : UUID = Field(...)
    email : EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name : str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birthday: Optional [date] = Field(default=None)

class UserRegister(User,UserLogin):
    pass

class Tweet(BaseModel):
    tweet_id : UUID = Field(...)
    content : str = Field(
        ...,
        min_length=1,
        max_length=256,
        )
    created_at : datetime = Field(default= datetime.now())
    updated_at : Optional[datetime] = Field(default= datetime.now())
    by : User = Field(...)

# Path Operations

## Users
### Register a user
@app.post(
    path = "/signup",
    response_model=User,
    status_code= status.HTTP_201_CREATED,
    summary="Register a User",
    tags= ['Users']
)
def signup(
    user:UserRegister = Body(...)
):
    """Signup
    
    This path operation register a user in the app

    Parameters:
        - Request body  parameter
            - user: UserRegister

    Returns a json whit the basic user information
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birthdate : date
    """
    with open('users.json',"r+",encoding="utf-8") as f:
        result = json.loads(f.read())
        tweet_dict = user.dict()
        tweet_dict['user_id'] = str (tweet_dict['user_id'])
        tweet_dict['birthday'] = str (tweet_dict['birthday'])
        result.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(result))
        return user


### User Login
@app.post(
    path = "/login",
    response_model=User,
    status_code= status.HTTP_200_OK,
    summary="Login a User",
    tags= ['Users']
)
def login(user:UserRegister = Body(...)):
    """Login
    
    This path operation register a user in the app

    Parameters:
        - Request body parameter
            - user: UserRegister

    Returns a json whit the basic user information
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name : str
        - birthdate : date
    """
    with open('users.json','r',encoding='utf-8') as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        for us in results:
            if us['email'] == user_dict['email']:
                if us['password'] == user_dict['password']:
                    return us
                else:
                    # return "User's password doesn't match"
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User's password doesn't match"
                        )
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User_id not found"
            )
    
    

### Show all the Users
@app.get(
    path = "/users",
    response_model=List[User],
    status_code= status.HTTP_200_OK,
    summary="Show all users",
    tags= ['Users']
)
def show_all_users():
    """ Show all users

    This path operation shows all users on the app

    Parameters:
        -
    
    Returns a json with the basic tweet information keys
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birthdate : date
    """
    with open('users.json','r',encoding='utf-8') as f:
        results = json.loads(f.read())
        return results


### Show a User
@app.get(
    path = "/users/{user_id}",
    response_model=User,
    status_code= status.HTTP_200_OK,
    summary="Show a User",
    tags= ['Users']
)
def show_a_user(
    user_id : str = Path(
        ...,
        title= "Show a Person details",
        description="this is the id number.in a format UUID"
        )
):
    """ Show a Users

    This path operation show a user in the app

    Parameters:
        - user_id
    
    Returns a json with the basic user information, keys
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birthdate : date
    """
    with open('users.json','r') as f:
        results = json.loads(f.read())
        for us in results:
            if(us['user_id'] == user_id):
                return us

    return user_id


### Delete a User
@app.delete(
    path = "/users/{user_id}/delete",
    response_model=List [User],
    status_code= status.HTTP_200_OK,
    summary="Delete a User",
    tags= ['Users']
)
def delete_a_user(
    user_id : str = Path(
        ...,
        title= "Deletes a Person",
        description="Delete the account from the app"
        )
):
    with open('users.json','r+') as f:
        results = json.loads(f.read())
        for i, us in enumerate(results):
            if(us['user_id'] == user_id):
                results.pop(i)
                with open('users.json','w') as fd:
                    fd.write(json.dumps(results))

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User_id not found"
        )

    
        
        


### Update a User
@app.put(
    path = "/users/{user_id}/update",
    response_model=User,
    status_code= status.HTTP_200_OK,
    summary="Update a User",
    tags= ['Users']
)
def update_a_user(new_user : User = Body(...)):
    with open('users.json','r+') as f:
        results = json.loads(f.read())
        user_dict = new_user.dict()
        for i, us in enumerate(results):
            if us["user_id"]==user_dict["user_id"]:
                user_dict['user_id'] = str(user_dict['user_id'])
                user_dict['birthday'] = str(user_dict['birthday'])
                results.pop(i)
                results.append(user_dict)
                f.seek(0)
                f.write(json.dumps(results))
                return new_user
                
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User_id not found"
        )
    


## Tweets

### Show all Tweets
@app.get(
    path ='/',
    response_model=List[Tweet],
    status_code= status.HTTP_200_OK,
    summary="Show all tweets",
    tags= ['Tweets']
    )
def home():
    """ Show all Tweets

    This path operation shows all the tweets

    Parameters:
        - 
    
    Returns a json with all tweets in the app, with the following keys
        - tweet_id : UUID 
        - content : str
        - created_at : datetime 
        - updated_at : Optional[datetime] 
        - by : User 
    """
    with open('tweets.json','r',encoding='utf-8') as f:
        results = json.loads(f.read())
        return results


### Post a tweet
@app.post(
    path ='/tweet/post',
    response_model=Tweet,
    status_code= status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags= ['Tweets']
    )
def post_tweet(tweet : Tweet = Body(...)):
    """ Post a Tweet

    This path operation post a new tweet in the app

    Parameters:
        - tweet : Tweet
    
    Returns a json with all users on the app, with the following keys
        - tweet_id : UUID 
        - content : str
        - created_at : datetime 
        - updated_at : Optional[datetime] 
        - by : User 
    """
    with open('tweets.json',"r+",encoding="utf-8") as f:
        result = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str (tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str (tweet_dict['created_at']) 
        tweet_dict['updated_at'] = str (tweet_dict['updated_at'])
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])
        tweet_dict['by']['birthday'] = str(tweet_dict['by']['birthday'])

        result.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(result))
        return tweet

### Show a Tweet
@app.get(
    path ='/tweet/{tweet_id}',
    response_model=Tweet,
    status_code= status.HTTP_200_OK,
    summary="Show a tweet",
    tags= ['Tweets']
    )
def show_tweet():
    pass

### Delete a Tweet
@app.delete(
    path ='/tweet/{tweet_id}/delete',
    response_model=Tweet,
    status_code= status.HTTP_200_OK,
    summary="Delete a tweet",
    tags= ['Tweets']
    )
def delete_tweet():
    pass


### Update a Tweet
@app.put(
    path ='/tweet/{tweet_id}/update',
    response_model=Tweet,
    status_code= status.HTTP_200_OK,
    summary="Update a tweet",
    tags= ['Tweets']
    )
def update_tweet():
    pass




