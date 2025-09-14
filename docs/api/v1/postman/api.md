{
	"info": {
		"_postman_id": "e1a8d4f7-0819-40cb-b8a1-73e699d4f070",
		"name": "Learnfolio API",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "42846789",
		"_collection_link": "https://learnfolio.postman.co/workspace/learnfolio-Workspace~7abb4d86-ebb2-4f27-893c-338a8882106f/collection/42846789-e1a8d4f7-0819-40cb-b8a1-73e699d4f070?action=share&source=collection_link&creator=42846789"
	},
	"item": [
		{
			"name": "accounts",
			"item": [
				{
					"name": "auth",
					"item": [
						{
							"name": "submit-identity",
							"protocolProfileBehavior": {
								"disabledSystemHeaders": {}
							},
							"request": {
								"auth": {
									"type": "noauth"
								},
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"amiiiriii.lamk.10@gmail.com\",\r\n    \"cf-turnstile-response\": \"token\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://localhost:8000/api/accounts/v1/auth/submit-identity/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"auth",
										"submit-identity",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "verify-otp",
							"request": {
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"amiiiriii.lamk.10@gmail.com\",\r\n    \"otp\": \"111111\",\r\n    \"cf-turnstile-response\": \"token\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://localhost:8000/api/accounts/v1/auth/verify-otp/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"auth",
										"verify-otp",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "login-password",
							"request": {
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"amiiiriii.lamk.10@gmail.com\",\r\n    \"password\": \"amir1234\",\r\n    \"cf-turnstile-response\": \"token\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://localhost:8000/api/accounts/v1/auth/login-password/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"auth",
										"login-password",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "verify-link",
							"request": {
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"amiiiriii.lamk.10@gmail.com\",\r\n    \"token\": \"eyJlbWFpbCI6ImFtaWlpcmlpaS5sYW1rLjEwQGdtYWlsLmNvbSIsInB1cnBvc2UiOiJyZWdpc3RlciJ9.aIUDTw.Hzmv3ehL4PFlxL21IF6ZKcoxvuE\",\r\n    \"cf-turnstile-response\": \"token\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://localhost:8000/api/accounts/v1/auth/verify-link/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"auth",
										"verify-link",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "token/refresh",
							"request": {
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"refresh\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NDgxOTk2NSwiaWF0IjoxNzU0MjE1MTY1LCJqdGkiOiIwZDY4NDRhYmE5MjU0YWNkODExNDVhYWNjNTI3Yzc2ZCIsInVzZXJfaWQiOjR9.z11jECIxyOje_AYHD6UFQTxncwpEkJcOEehWzljF3zk\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://localhost:8000/api/accounts/v1/auth/token/refresh/",
									"protocol": "http",
									"host": [
										"localhost"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"auth",
										"token",
										"refresh",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "logout",
							"request": {
								"method": "POST",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0NDE0MjcwLCJpYXQiOjE3NTQ0MTMzNzAsImp0aSI6Ijk4YWMwMDc3MjJhNjRmNGNiOWYzNjU0Yzk5MGU3MzE3IiwidXNlcl9pZCI6NH0._llz8RIlR_cdKbKw8NOXrgiMcLEiJreP4-6wD1idf44",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"refresh\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NTAxODE3MCwiaWF0IjoxNzU0NDEzMzcwLCJqdGkiOiJkZTg1ZDZkYWExMmU0N2EwOTlmOTViMTE5YjE0NDljNiIsInVzZXJfaWQiOjR9.ENiIZxQCL1aMLKGPRsl2_DRBJgP6-ZEwN83XBUxmrj4\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/auth/logout/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"auth",
										"logout",
										""
									]
								}
							},
							"response": []
						}
					]
				},
				{
					"name": "password",
					"item": [
						{
							"name": "request-password-reset",
							"request": {
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"09111111111\",\r\n    \"cf-turnstile-response\": \"token\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/password/request-password-reset/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"password",
										"request-password-reset",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "otp-verification-password-reset",
							"request": {
								"auth": {
									"type": "noauth"
								},
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"09111111111\",\r\n    \"cf-turnstile-response\": \"token\",\r\n    \"otp\": \"726216\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/password/verify-otp/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"password",
										"verify-otp",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "link-verification-password-reset",
							"request": {
								"auth": {
									"type": "noauth"
								},
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"amiiiriii.lamk.10@gmail.com\",\r\n    \"cf-turnstile-response\": \"token\",\r\n    \"token\": \"eyJlbWFpbCI6ImFtaWlpcmlpaS5sYW1rLjEwQGdtYWlsLmNvbSIsInB1cnBvc2UiOiJyZXNldF9wYXNzd29yZCJ9.aKYKSw.w_lXcr15T8z-LiYRkC1D-Vl4gKA\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/password/verify-link/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"password",
										"verify-link",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "change-password",
							"request": {
								"auth": {
									"type": "noauth"
								},
								"method": "POST",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1NzIxOTYwLCJpYXQiOjE3NTU3MjEwNjAsImp0aSI6IjRmNDJkYWY3NDQyNjRjMzhiYTFjMTU2NjI1Mjg4ZmU1IiwidXNlcl9pZCI6OX0.xCdcRhINiJ4O1tGn5fbAgaH8T_OzukOdnbuyo-v74J8",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"old_password\": \"amir_1382\",\r\n    \"new_password\": \"amir_1382\",\r\n    \"confirm_password\": \"amir_1382\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/password/change-password/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"password",
										"change-password",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "reset-password",
							"request": {
								"auth": {
									"type": "noauth"
								},
								"method": "POST",
								"header": [],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"cf-turnstile-response\": \"token\",\r\n    \"reset_token\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IjA5MTExMTExMTExIiwidHlwZSI6InJlc2V0X3Bhc3N3b3JkIiwiZXhwIjoxNzU1Nzc0ODkzLCJpYXQiOjE3NTU3NzMwOTN9.d9iW7sXtITk6X_hNKvxRR_Q-VM_sFS3upenqROgv3h0\",\r\n    \"new_password\": \"amir_1382\",\r\n    \"confirm_password\": \"amir_1382\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/password/reset-password/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"password",
										"reset-password",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "first-time-password",
							"request": {
								"auth": {
									"type": "noauth"
								},
								"method": "POST",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1NzE0MTM5LCJpYXQiOjE3NTU3MTMyMzksImp0aSI6IjNiYzM4YjkzODYxYjQ5ZGQ5MjFmYzE0OTEwOTM4ZDQ1IiwidXNlcl9pZCI6OX0.Bd3Du1nE4ZfMFNX4tJDjg7Ouk3KYKaqRyD9r2zuHMQM",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"new_password\": \"amir_1382\",\r\n    \"confirm_password\": \"amir_1382\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/password/first-time-password/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"password",
										"first-time-password",
										""
									]
								}
							},
							"response": []
						}
					]
				},
				{
					"name": "profile",
					"item": [
						{
							"name": "profile",
							"request": {
								"method": "GET",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NjMzMDIzLCJpYXQiOjE3NTY2MzIxMjMsImp0aSI6ImU3OTlmYTliNTJhZjQ3MjZhYjQ0MThlNjU3ZTQxNjBkIiwidXNlcl9pZCI6OH0.JQG4uMgfB1nhrsrniETvov1MzDGiO3TXMG9iWrKRqhw",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/profile/me/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"profile",
										"me",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "update profile",
							"request": {
								"method": "PATCH",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NjMzMDIzLCJpYXQiOjE3NTY2MzIxMjMsImp0aSI6ImU3OTlmYTliNTJhZjQ3MjZhYjQ0MThlNjU3ZTQxNjBkIiwidXNlcl9pZCI6OH0.JQG4uMgfB1nhrsrniETvov1MzDGiO3TXMG9iWrKRqhw",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"full_name\": \"amir\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/profile/me/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"profile",
										"me",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "delete accounte",
							"request": {
								"method": "DELETE",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NjMzOTM5LCJpYXQiOjE3NTY2MzMwMzksImp0aSI6IjZkMDYzMmQzMzk1YjRlNjI5Y2Q1MTQzZWEyYjU1NWIxIiwidXNlcl9pZCI6OH0.Z80pxDDYBCDu0jgbUKI729A4MahSnlxNxNzoa6-3msQ",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/profile/me/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"profile",
										"me",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "profile admin",
							"request": {
								"method": "GET",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NjM2MzU5LCJpYXQiOjE3NTY2MzU0NTksImp0aSI6ImY5MTQ0ZGU5YzQ2NDQ5ZDY4MTVlMGJjOTRmYTUxYmJhIiwidXNlcl9pZCI6Mn0.6XdUbbsKnA535nVHjC5ZXn6zn7dBlvFj5f6J7urODns",
										"type": "text"
									}
								],
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/profile/admin/me/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"profile",
										"admin",
										"me",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "update profile admin",
							"request": {
								"method": "PATCH",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NzE3NjE4LCJpYXQiOjE3NTY3MTY3MTgsImp0aSI6ImY1NzA2ODlhOWEzNTQzOTdiZGUzZGVmMzRiMTdmMTc1IiwidXNlcl9pZCI6Mn0.Kt-nq54N5IHE54N7osQPAhy8nqRCCJuNTIItB9azezs",
										"type": "text"
									}
								],
								"body": {
									"mode": "formdata",
									"formdata": [
										{
											"key": "description",
											"value": "hi",
											"description": "string",
											"type": "text"
										},
										{
											"key": "social_networks",
											"value": "{\"github\": \"https://github.com/amirhosei004\"}",
											"description": "jsonfield",
											"type": "text"
										},
										{
											"key": "image",
											"description": "file image",
											"type": "file",
											"src": "postman-cloud:///1f0869aa-138b-48a0-b3e7-c3271771374b"
										}
									]
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/profile/admin/me/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"profile",
										"admin",
										"me",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "update email or phone",
							"request": {
								"method": "PATCH",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NjM4MjE0LCJpYXQiOjE3NTY2MzczMTQsImp0aSI6IjdjOTcwNDUwMmU2MTRjZmI5NjQyMWFjNmIxM2ZjMzFlIiwidXNlcl9pZCI6Mn0.XLZAN_IW_hEFzSl6F-l7D5mlEhyk4ojisZ2eIs1Ro3s",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"09111114411\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/profile/update-identity/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"profile",
										"update-identity",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "confirm update phone",
							"request": {
								"method": "PATCH",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NjM4MjE0LCJpYXQiOjE3NTY2MzczMTQsImp0aSI6IjdjOTcwNDUwMmU2MTRjZmI5NjQyMWFjNmIxM2ZjMzFlIiwidXNlcl9pZCI6Mn0.XLZAN_IW_hEFzSl6F-l7D5mlEhyk4ojisZ2eIs1Ro3s",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"09111114411\",\r\n    \"otp\": \"040612\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/profile/update-phone/verify/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"profile",
										"update-phone",
										"verify",
										""
									]
								}
							},
							"response": []
						},
						{
							"name": "confirm update email",
							"request": {
								"method": "PATCH",
								"header": [
									{
										"key": "Authorization",
										"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NjM3Mjc1LCJpYXQiOjE3NTY2MzYzNzUsImp0aSI6IjI0Nzg0ODU4YzM0YzQ2YmFiN2EwZWEwOWIyMDNkZTljIiwidXNlcl9pZCI6Mn0.15sfZ2-xEoTuHnPbLE_Y_08sej19RTsxDDVlzUaMmC4",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\r\n    \"identity\": \"amiiiriii.lamk.10@gmail.com\",\r\n    \"token\": \"eyJlbWFpbCI6ImFtaWlpcmlpaS5sYW1rLjEwQGdtYWlsLmNvbSIsInB1cnBvc2UiOiJ1cGRhdGVfaWRlbnRpdHkifQ.aLQleA.khh0vyI2iDlm0CB3wjc_ld30_zQ\"\r\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "http://127.0.0.1:8000/api/accounts/v1/profile/update-email/confirm/",
									"protocol": "http",
									"host": [
										"127",
										"0",
										"0",
										"1"
									],
									"port": "8000",
									"path": [
										"api",
										"accounts",
										"v1",
										"profile",
										"update-email",
										"confirm",
										""
									]
								}
							},
							"response": []
						}
					]
				}
			]
		},
		{
			"name": "blog",
			"item": [
				{
					"name": "list blogs",
					"request": {
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/blog/v1/blogs/?search=tet&page=1",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"blog",
								"v1",
								"blogs",
								""
							],
							"query": [
								{
									"key": "search",
									"value": "tet"
								},
								{
									"key": "page",
									"value": "1"
								}
							]
						}
					},
					"response": []
				},
				{
					"name": "create blog",
					"request": {
						"method": "POST",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NzE0NzkyLCJpYXQiOjE3NTY3MTM4OTIsImp0aSI6IjM3MzIyNThiMDY0ZjRjZDc4ZWFlNjQ1NDlmNzE0N2NkIiwidXNlcl9pZCI6Mn0.Aqyj95MUip4CKD-sCC3NOJ0Emn35R7reRNArbXVWi_I",
								"type": "text"
							}
						],
						"body": {
							"mode": "formdata",
							"formdata": [
								{
									"key": "title",
									"value": "سلام علیک",
									"description": "string",
									"type": "text"
								},
								{
									"key": "content",
									"value": "کسشر پروژه است ایا",
									"description": "string",
									"type": "text"
								},
								{
									"key": "image",
									"description": "file",
									"type": "file",
									"src": "postman-cloud:///1f0869aa-1202-4790-9c60-e188b8040528"
								}
							]
						},
						"url": {
							"raw": "http://localhost:8000/api/blog/v1/blogs/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"blog",
								"v1",
								"blogs",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "detail blog",
					"request": {
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/blog/v1/blogs/tetetgrerg-tgtg/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"blog",
								"v1",
								"blogs",
								"tetetgrerg-tgtg",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "update blog",
					"request": {
						"method": "PUT",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NzIyNTI5LCJpYXQiOjE3NTY3MjE2MjksImp0aSI6IjVjZmE4ZDBjMGJiZTQ3ZTBiYjA5ZTEzODA5ZTk5ZDg5IiwidXNlcl9pZCI6Mn0.YwC6Zxh2BDWMrR0EK-tMIpwdmYi88AhjF6hCfU8z-tM",
								"type": "text"
							}
						],
						"body": {
							"mode": "formdata",
							"formdata": [
								{
									"key": "title",
									"value": "test",
									"description": "string",
									"type": "text"
								},
								{
									"key": "content",
									"value": "test",
									"description": "string",
									"type": "text"
								},
								{
									"key": "image",
									"description": "file",
									"type": "file",
									"src": "postman-cloud:///1f0869d0-78a0-4a80-97fc-66d1b05cd33a"
								}
							]
						},
						"url": {
							"raw": "http://localhost:8000/api/blog/v1/blogs/tet/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"blog",
								"v1",
								"blogs",
								"tet",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "update blog",
					"request": {
						"method": "PATCH",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NjY3NjU1LCJpYXQiOjE3NTY2NjY3NTUsImp0aSI6Ijg5YjQ1NWI0ZTZkMDQ4OTJiY2U2YzQ1MmYwY2FjOTVhIiwidXNlcl9pZCI6Mn0.43lKyXBuyJZwH8xsxCe1UDzAU0fnegAHb2bW3oHPvpI",
								"type": "text"
							}
						],
						"body": {
							"mode": "formdata",
							"formdata": [
								{
									"key": "title",
									"value": "test2",
									"description": "string",
									"type": "text"
								}
							]
						},
						"url": {
							"raw": "http://localhost:8000/api/blog/v1/blogs/test/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"blog",
								"v1",
								"blogs",
								"test",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "delete blog",
					"request": {
						"method": "DELETE",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NzEzODgxLCJpYXQiOjE3NTY3MTI5ODEsImp0aSI6IjUwOTU3NDFhN2ZmMzQ3ZWViZjI2MmE2MzVlMWFlYzIzIiwidXNlcl9pZCI6Mn0.fKJQKnPxbPlsIrsZF8qDph9BArpmT37tW3L1NYadwq0",
								"type": "text"
							}
						],
						"url": {
							"raw": "http://localhost:8000/api/blog/v1/blogs/بلیلفل65745ل-ف55/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"blog",
								"v1",
								"blogs",
								"بلیلفل65745ل-ف55",
								""
							]
						}
					},
					"response": []
				}
			]
		}
	]
}