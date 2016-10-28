import numpy as np
import pandas as pd


def parse_tickets(tickets_col):
    parsed = pd.DataFrame(columns=['avg_ticket_price',
                                   'max_ticket_price',
                                   'ticket_tiers',
                                   'total_available'])
    for row in tickets_col:
        if row != []:
            num_tickets = sum([ticket.get('quantity_total') for ticket in row])
            max_price = max([ticket.get('cost', 0) for ticket in row])
            ticket_tiers = len(row)
            weighted_prices = sum([ticket.get('cost', 0) * \
                                   ticket.get('quantity_total', 0) \
                                   for ticket in row])
            if num_tickets == 0:
                avg_price = np.mean([ticket.get('cost', 0) for ticket in row])
            else:
                avg_price = weighted_prices / num_tickets
            key_data = pd.Series({'avg_ticket_price': avg_price,
                                  'max_ticket_price': max_price,
                                  'ticket_tiers': ticket_tiers,
                                  'total_available': num_tickets})
        else:
            key_data = pd.Series({'avg_ticket_price': 0.,
                                  'max_ticket_price': 0.,
                                  'ticket_tiers': 0,
                                  'total_available': 0})
        parsed = parsed.append(key_data, ignore_index=True)
    parsed['ticket_tiers'] = parsed['ticket_tiers'].astype(int)
    parsed['total_available'] = parsed['ticket_tiers'].astype(int)
    return parsed


def parse_caps(column):
    pct_vect = np.array([])
    for row in column:
        caps = 0
        if row == '':
            pct_caps = 0
        else:
            for char in row:
                if char == char.upper():
                    caps += 1
            pct_caps = float(caps) / len(row)
        pct_vect = np.append(pct_vect, pct_caps)
    return pct_vect


def scrub_df(df):
    # label the fraud cases
    df['fraud'] = ((df['acct_type'] == 'fraudster') | \
                  (df['acct_type'] == 'fraudster_event') | \
                  (df['acct_type'] == 'fraudster_att')).astype(int)

    # fill 'has_header' field with 0.
    df['has_header'] = df[['has_header']].fillna(0.)
    # boolean flag on whether field is empty string

    df['org_desc_bool'] = (df['org_desc'] == '').astype(int)
    # extract info from ticket_types

    df = pd.concat([df, parse_tickets(df['ticket_types'])], axis=1)
    # percentage of capital letters in 'name'

    df['pct_caps'] = parse_caps(df['name'])

    # previous_payouts: replace with len(list)
    df['previous_payouts'] = df['previous_payouts'].apply(len)

    # venue_address: boolean blank/not blank
    df['blank_venue_address'] = 0
    mask = df['venue_name'] == ''
    df.loc[mask,'blank_venue_address'] = 1

    # drop venue_country, make boolean venue_country == country
    df['same_countries'] = 0
    mask = df['country']==df['venue_country']
    df.loc[mask,'same_countries'] = 1

    # venue_name: create boolean was nan/not nan
    df['nan_venue'] = 0
    df.loc[df['venue_name'].isnull(),'nan_venue'] = 1
    # venue_name: create boolean is blank/not blank
    df['venue_name'].fillna('')
    df['blank_venue_name'] = 0
    mask = df['venue_name'] == ''
    df.loc[mask,'blank_venue_name'] = 1

    # 'listed' map to boolean
    df['listed'] = df['listed'].map({'y':1, 'n':0})
    # drop 'object_id'
    df.drop('object_id', axis=1, inplace=True)
    # create 'org_facebook_nan'
    df['org_facebook_nan'] = df['org_facebook'].isnull().map({True:1, False:0})
    # fill 'org_facebook' nulls
    df['org_facebook'] = df['org_facebook'].fillna(0.)
    # create 'org_twitter_nan'
    df['org_twitter_nan'] = df['org_twitter'].isnull().map({True:1, False:0})
    # fill 'org_twitter' nulls
    df['org_twitter'] = df['org_twitter'].fillna(0.)
    # flag 'payee_name' blanks
    df['payee_name'] = (df['payee_name'] == '').map({True:1, False:0})
    # flag 'org_name' blanks
    df['org_name'] = (df['org_name'] == '').map({True:1, False:0})
    # flag 'org_desc' blanks
    df['org_desc'] = (df['org_desc'] == '').map({True:1, False:0})

    df['delivery_method'] = df['delivery_method'].astype(str)
    df['time_to_pay'] = df['approx_payout_date'] - df['event_start']
    df['time_to_pay2'] = df['approx_payout_date'] - df['event_created']
    df['planning_time'] = df['approx_payout_date'] - df['event_start']
    df['duration'] = df['event_end'] - df['event_start']
    df['event_published'].fillna(0, inplace=True)
    df['has_pub_date'] = df['event_published'] != 0
    df['has_pub_date'] = df['has_pub_date'].astype(int)
    drop_cols = ['sale_duration', 'user_created', 'user_type', 'ticket_types',
                 'venue_address', 'venue_latitude', 'venue_longitude',
                 'venue_country','venue_name', 'venue_state', 'payout_type',
                 'email_domain','description', 'approx_payout_date',
                 'event_start','event_end', 'event_published', 'event_created',
                 'currency','country', 'delivery_method', 'acct_type', 'name']
    df.drop(drop_cols, axis=1, inplace=True)
    return df

if __name__ == '__main__':

    df = pd.read_json('data/data.json')
    df = scrub_df(df)
