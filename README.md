# Build a Blockchain Fee Reporter Service (Bitpanda interview assignment)

This is a coding task designed to be used for hiring Python engineers to Bitpandas Blockchain team. The aim is to help 
both the applicant and the hiring Manager understand if a candidate will be a good fit for working in the team. 

## Introduction
One of the responsibilities of the Bitpanda Blockchain team is to keep track of fees of various blockchains.
Depending on various levels of seniority, we will review the finished task under different aspects. 

Please commit your changes before the scheduled interview, regardless of the state of completion. 

## Task description
Your task is to create a python service that retrieves and reports the fees per transaction of two sample blockchains:
* Bitcoin (unit: BTC)
* Binance Smart Chain (unit: BNB).

### Functional Requirements
Every 10 seconds the service needs to:
1. query the provided endpoints for fees
2. calculate an estimated fee per transaction
3. report the fee by logging them in the following format
```
Fee for <blockchain network> at <iso datetime>: <fee> <unit>
```
for example:
```
Fee for Bitcoin at 2023-05-18T15:17:00+00:00: 0.00012 BTC
```

Also, the service should:
1. start by running a single console command
2. stop gracefully when receiving a SIGTERM or SIGINT signal

### Non-Functional Requirements
1. There needs to be a clear separation of concerns between:
   1. The scheduler (10 seconds periodic process)
   2. The fee retrieval by querying the resources
   3. The fee calculation
   4. The reporting of fee
2. The fee calculation (your business logic) needs to be properly unit tested
3. The fee retrieval needs to be error handled for cases of broken connection etc.
4. Modify this README to provide clear instructions on how to run the service locally

## Resources

Blockchain Networks required:

### Bitcoin
- name: Bitcoin
- unit: BTC
- fee endpoint: https://bitcoiner.live/api/fees/estimates/latest
- fee API documentation: https://bitcoiner.live/doc/api

Additional info: For Bitcoin you should estimate the fee a transaction of `size = 140 vB` should pay
to be included in the next 3 blocks.

### Binance Smart Chain (BSC)
- name: BSC
- unit: BNB
- node url: https://bsc.publicnode.com/
- fee rpc method: `eth_maxPriorityFeePerGas`
- tip: base fee on binance chain can be assumed as 0 and irrelevant here

Additional info: For BSC you should calculate the fee for a transaction with `gas_limit = 55000` to be included
in a block as quickly as possible.

### Dependencies
We provide a sample `pyproject.toml` file as a starting point. You are encouraged but not required to use `poetry`
as your package manager.

## Extra points 1 (Medior level)
1. Dockerize the application
2. Integrate an additional network of your choice

## Extra points 2 (Senior level)
1. Utilize `asyncio` to make non-blocking network calls
2. Implement a caching layer that doesn't report the fee if it is the same as the previous one
